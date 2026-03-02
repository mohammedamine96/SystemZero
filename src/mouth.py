import os
import time
import threading

class Mouth:
    def __init__(self):
        print(">> [MOUTH] Initializing Next-Gen Audio (Neural TTS)...")
        try:
            import pygame
            # Initialize the audio mixer
            pygame.mixer.init()
            # "en-GB-RyanNeural" is a highly realistic, professional British male voice. 
            # You can also try "en-US-ChristopherNeural" or "en-US-AriaNeural"
            self.voice = "en-CA-ClaraNeural" 
            print(">> [MOUTH] Neural Vocal Cords Online.")
        except Exception as e:
            print(f">> [MOUTH ERROR] Failed to initialize audio: {e}")

    def speak(self, text, wait=False):
        """Generates realistic speech and plays it smoothly."""
        if not text: return
        
        def _speak_thread():
            try:
                import pygame
                # Clean the text so command-line quotes don't break it
                safe_text = text.replace('"', '').replace("'", "")
                output_file = "response.mp3"
                
                # 1. Generate the high-definition audio file using Edge-TTS
                # (This reaches out to Azure's Neural TTS servers instantly)
                os.system(f'edge-tts --voice {self.voice} --text "{safe_text}" --write-media {output_file}')
                
                # 2. Load and play the audio file
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                
                # 3. Wait for the audio to finish playing
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                # 4. Cleanup: Unload and delete the temporary audio file
                pygame.mixer.music.unload()
                try:
                    os.remove(output_file)
                except:
                    pass
                    
            except Exception as e:
                print(f">> [MOUTH ERROR] Neural Speech Failed: {e}")

        # If the system needs to wait for the speech to finish before moving on
        if wait:
            _speak_thread()
        else:
            # Otherwise, speak in the background
            t = threading.Thread(target=_speak_thread, daemon=True)
            t.start()