import os
import threading
import time
import speech_recognition as sr
from faster_whisper import WhisperModel
import pvporcupine
from pvrecorder import PvRecorder
import winsound

class Ears:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.is_listening = True
        self.active_session = False
        self.is_busy = False  # The Mute Switch!

        print(">> [EARS] Initializing Porcupine Wake-Word (Trigger: 'Start')...")
        try:
            self.picovoice_key = os.getenv("PICOVOICE_API_KEY")
            keyword_path = os.path.join("models", "start.ppn")
            
            self.porcupine = pvporcupine.create(
                access_key=self.picovoice_key,
                keyword_paths=[keyword_path]
            )

            self.recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)

            print(">> [EARS] Initializing Whisper Neural Engine (Local)...")
            self.model = WhisperModel("base.en", device="cpu", compute_type="int8")
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()

            print(">> [EARS] Auditory Cortex Online. Awaiting the wake word 'Start'.")

            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()

        except Exception as e:
            print(f">> [EARS CRITICAL ERROR] Failed to initialize: {e}")

    def _listen_loop(self):
        self.recorder.start()
        
        while self.is_listening:
            # 🛑 THE MUTE SWITCH: Pause the ears while System Zero is speaking!
            if self.is_busy:
                time.sleep(0.1)
                continue

            if not self.active_session:
                # --- STATE 1: STANDBY MODE (Waiting for 'Start') ---
                try:
                    pcm = self.recorder.read()
                    keyword_index = self.porcupine.process(pcm)

                    if keyword_index >= 0:
                        print("\n>> [WAKE WORD DETECTED] Entering Active Session...")
                        winsound.Beep(800, 200) 
                        self.active_session = True
                        
                        # Safely stop the watchdog and yield the microphone
                        self.recorder.stop()
                        time.sleep(0.3) # <--- THE FIX: Give Windows time to release the hardware lock!
                except Exception as e:
                    print(f">> [EARS STANDBY GLITCH] {e}")
                    time.sleep(0.5)
            else:
                # --- STATE 2: ACTIVE SESSION (Continuous Conversation) ---
                command = self._record_and_transcribe()
                
                if command:
                    # Check if the user wants to end the conversation manually
                    if any(phrase in command.lower() for phrase in ["sleep", "stop listening", "goodbye", "nevermind"]):
                        print("\n>> [EARS] Going to sleep. Awaiting 'Start'...")
                        winsound.Beep(600, 200) 
                        self.active_session = False
                        time.sleep(0.3) # <--- THE FIX: Yield microphone back to watchdog
                        self.recorder.start()
                    else:
                        # Send command to the Brain
                        self.command_queue.put(command)
                        # Give the Brain 1 full second to trigger the "is_busy" mute switch
                        time.sleep(1.0) 
                else:
                    # If the user is silent for 5 seconds, auto-sleep!
                    print("\n>> [EARS] Silence detected. Returning to Standby...")
                    self.active_session = False
                    time.sleep(0.3) # <--- THE FIX: Yield microphone back to watchdog
                    try:
                        self.recorder.start()
                    except Exception as e:
                        print(f">> [EARS RESTART ERROR] Could not grab microphone: {e}")

    def _record_and_transcribe(self):
        with self.microphone as source:
            try:
                print(">> [LISTENING] (Speak now or remain silent to sleep)...")
                # Shorter ambient calibration so it feels more responsive
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)

                temp_file = "workspace/temp_voice.wav"
                os.makedirs("workspace", exist_ok=True)
                
                with open(temp_file, "wb") as f:
                    f.write(audio.get_wav_data())

                segments, _ = self.model.transcribe(temp_file, beam_size=5)
                transcription = "".join([segment.text for segment in segments]).strip()

                if os.path.exists(temp_file):
                    os.remove(temp_file)

                if transcription:
                    # Filter out random background noise that Whisper sometimes hallucinates
                    if len(transcription) > 2: 
                        print(f">> [HEARD]: {transcription}")
                        return transcription
                return None

            except sr.WaitTimeoutError:
                return None
            except Exception as e:
                print(f">> [WHISPER GLITCH] {e}")
                return None