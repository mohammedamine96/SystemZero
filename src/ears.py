import os
import threading
import speech_recognition as sr
from faster_whisper import WhisperModel

class Ears:
    def __init__(self, command_queue):
        self.command_queue = command_queue
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = True

        print(">> [EARS] Initializing Whisper Neural Engine (Local)...")
        try:
            # "base.en" is incredibly fast and highly accurate for English.
            # It will download the model (~140MB) to your PC on the very first run.
            self.model = WhisperModel("base.en", device="cpu", compute_type="int8")
            
            print(">> [EARS] Whisper Engine Online. Calibrating ambient room noise...")
            with self.microphone as source:
                # Dynamically adjusts to your room's background noise (fans, AC, etc.)
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
            print(">> [EARS] Auditory Cortex fully calibrated. Awaiting the wake word 'Zero'.")
            
            # Start the background listening thread
            self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.listen_thread.start()
            
        except Exception as e:
            print(f">> [EARS CRITICAL ERROR] Failed to initialize: {e}")

    def _listen_loop(self):
        with self.microphone as source:
            while self.is_listening:
                try:
                    # Waits in the background until you speak, then captures the audio
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=15)
                    
                    # Save audio to a temporary buffer for Whisper
                    temp_file = "workspace/temp_voice.wav"
                    with open(temp_file, "wb") as f:
                        f.write(audio.get_wav_data())

                    # Transcribe using the local neural network
                    segments, info = self.model.transcribe(temp_file, beam_size=5)
                    transcription = "".join([segment.text for segment in segments]).strip()

                    if transcription:
                        clean_text = transcription.lower()
                        
                        # Only react if the wake word "zero" is spoken
                        if "zero" in clean_text:
                            print(f"\n>> [HEARD]: {transcription}")
                            
                            # Strip "zero" and punctuation from the command
                            command = clean_text.replace("zero", "", 1).strip(" .,?!")
                            
                            if command:
                                # Inject the spoken command directly into the brain's queue!
                                self.command_queue.put(command)

                    # Cleanup the temporary audio file
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f">> [EARS WARNING] Audio processing glitch: {e}")