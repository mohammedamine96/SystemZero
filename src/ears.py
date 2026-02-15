import speech_recognition as sr
import sys

class Ears:
    def __init__(self):
        print(">> [EARS] Initializing Audio Drivers...")
        try:
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone()
            
            # Auto-calibration for room noise
            with self.mic as source:
                print(">> [EARS] Calibrating background noise... (Please remain silent)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.dynamic_energy_threshold = True
            print(">> [EARS] Online and Calibrated.")
            
        except OSError:
            print("\n[CRITICAL ERROR] No Microphone detected.")
            print("Ensure your microphone is plugged in and accessible.")
            # We don't exit here so the system can still run in text mode
            self.mic = None

    def listen(self):
        """
        Listens to the microphone and returns text.
        Returns: str (command) or None (silence/error)
        """
        if not self.mic:
            print(">> [EARS] Microphone not available.")
            return None

        with self.mic as source:
            print("\n>> [LISTENING] Speak now...", end="\r")
            try:
                # Listen with a timeout (don't hang forever)
                # phrase_time_limit prevents it from listening to infinite silence
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                print(">> [EARS] Processing...       ", end="\r")
                # Use Google's free API (requires internet)
                text = self.recognizer.recognize_google(audio)
                print(f">> [HEARD]: \"{text}\"")
                return text
                
            except sr.WaitTimeoutError:
                return None # Silence
            except sr.UnknownValueError:
                print(">> [EARS] Audio unintelligible.")
                return None
            except sr.RequestError as e:
                print(f">> [EARS] Connection Error: {e}")
                return None