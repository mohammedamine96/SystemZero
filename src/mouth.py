import os
import asyncio
import edge_tts
import pygame
import threading
import time

# SETTINGS
VOICE = "en-US-AriaNeural"
OUTPUT_FILE = "response.mp3"

class Mouth:
    def __init__(self):
        print(f">> [MOUTH] Initializing TTS Engine ({VOICE})...")
        try:
            pygame.mixer.init()
            print(">> [MOUTH] Vocal Cords Online.")
        except Exception as e:
            print(f">> [MOUTH] Audio Init Failed: {e}")

    def speak(self, text):
        if not text:
            return
        # Run in separate thread to avoid blocking the Brain
        threading.Thread(target=self._run_tts_thread, args=(text,)).start()

    def _run_tts_thread(self, text):
        try:
            # 1. CLEANUP: Unload and delete previous file to break locks
            if pygame.mixer.get_init():
                pygame.mixer.music.unload()
            
            if os.path.exists(OUTPUT_FILE):
                try:
                    os.remove(OUTPUT_FILE)
                except PermissionError:
                    print(">> [MOUTH] Warning: Audio file locked. Skipping this sentence.")
                    return

            # 2. GENERATE: Create new audio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            communicate = edge_tts.Communicate(text, VOICE)
            loop.run_until_complete(communicate.save(OUTPUT_FILE))

            # 3. VERIFY & PLAY
            if os.path.exists(OUTPUT_FILE):
                self._play_audio()
            else:
                print(">> [MOUTH ERROR] File failed to generate.")

        except Exception as e:
            print(f">> [MOUTH CRITICAL] {e}")

    def _play_audio(self):
        try:
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # STRICT CLEANUP to release file lock
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f">> [PLAYBACK ERROR] {e}")