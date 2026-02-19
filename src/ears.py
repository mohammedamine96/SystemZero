import speech_recognition as sr
import sys

class Ears:
    def __init__(self):
        print(">> [EARS] Initializing Audio Drivers...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibration for ambient noise
        with self.microphone as source:
            print(">> [EARS] Calibrating background noise... (Please remain silent)")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print(">> [EARS] Online and Calibrated.")

    def listen(self):
        """
        Active Listening: Listens for a full command (longer timeout).
        """
        try:
            with self.microphone as source:
                print(">> [EARS] Listening for command...", end="\r")
                # Listen for longer because this is the actual command
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print(">> [EARS] Processing audio...           ", end="\r")
            text = self.recognizer.recognize_google(audio)
            print(f">> [HEARD]: \"{text}\"")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"\n[EARS ERROR] {e}")
            return None

    def wait_for_wake_word(self, wake_word="zero"):
        """
        Passive Listening: Loops infinitely until the wake word is heard.
        """
        print(f">> [PASSIVE] Waiting for activation phrase: '{wake_word}'...")
        
        while True:
            try:
                with self.microphone as source:
                    # Short listen to catch the phrase quickly
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3)
                
                # We use show_all=False to get just the text
                try:
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # Check if the phrase was said
                    if wake_word in text:
                        print(f"\n>> [ACTIVATION] Detected '{text}'!")
                        return True
                    else:
                        print(f">> [IGNORED] '{text}'", end="\r")
                        
                except sr.UnknownValueError:
                    # Silence or noise, just ignore and loop back
                    continue
                    
            except KeyboardInterrupt:
                print("\n>> [EARS] Stopping...")
                return False
            except Exception as e:
                # If internet cuts out or mic fails, print and retry
                print(f"[PASSIVE ERROR] {e}", end="\r")
                continue