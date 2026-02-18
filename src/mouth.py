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

    def speak(self, text, wait=True):
        """
        Speaks the text.
        params:
            text (str): The text to speak.
            wait (bool): If True, the agent pauses execution until speech finishes.
        """
        if not text:
            return
        
        # If wait is True, we run directly (Blocking)
        # If wait is False, we spin up a thread (Non-Blocking)
        if wait:
            self._run_tts(text)
        else:
            threading.Thread(target=self._run_tts, args=(text,)).start()

    def _run_tts(self, text):
        try:
            # 1. CLEANUP (Critical for file locks)
            if pygame.mixer.get_init():
                pygame.mixer.music.unload()
            
            if os.path.exists(OUTPUT_FILE):
                try:
                    os.remove(OUTPUT_FILE)
                except PermissionError:
                    print(">> [MOUTH] Warning: Audio locked. Skipping.")
                    return

            # 2. GENERATE
            # We create a new loop for this specific generation task
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            communicate = edge_tts.Communicate(text, VOICE)
            loop.run_until_complete(communicate.save(OUTPUT_FILE))

            # 3. PLAY & WAIT
            if os.path.exists(OUTPUT_FILE):
                self._play_audio_blocking()
            
        except Exception as e:
            print(f">> [MOUTH ERROR] {e}")

    def _play_audio_blocking(self):
        try:
            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()
            
            # BLOCKING LOOP: Keeps the code stuck here until audio finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f">> [PLAYBACK ERROR] {e}")