import cv2
import easyocr
import numpy as np
import pyautogui
import threading
import time

class Vision:
    def __init__(self):
        print(">> [EYES] Initializing Optical Nerve (EasyOCR)...")
        # 'en' for English. gpu=True if you have NVIDIA, else False
        self.reader = easyocr.Reader(['en'], gpu=True) 
        self.screen_map = [] # Stores last known text locations
        self.lock = threading.Lock()
        print(">> [EYES] Vision Module Online.")

    def scan_screen(self):
        """
        Takes a snapshot and builds a text-coordinate map.
        Returns the raw map for debugging.
        """
        print(">> [EYES] Scanning current visual field...")
        
        # 1. Capture Screen
        screenshot = pyautogui.screenshot()
        
        # 2. Convert to format OpenCV/EasyOCR understands
        image = np.array(screenshot)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 3. Read Text (Async capable in v3.1, sync for now)
        # detail=0 returns just text; detail=1 returns coords
        results = self.reader.readtext(image)
        
        # 4. Update Spatial Map
        new_map = []
        for (bbox, text, prob) in results:
            if prob > 0.5: # Filter low confidence garbage
                # bbox is [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
                # We need the center point for clicking
                top_left = bbox[0]
                bottom_right = bbox[2]
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                
                new_map.append({
                    "text": text.lower(),
                    "x": center_x,
                    "y": center_y,
                    "raw_text": text
                })
        
        with self.lock:
            self.screen_map = new_map
            
        print(f">> [EYES] Index complete. Found {len(new_map)} elements.")
        return new_map

    def find_element(self, target_text):
        """
        Queries the spatial map for a specific keyword.
        Returns: {'x': int, 'y': int} or None
        """
        # Trigger a fresh scan if requested (or rely on cached for speed)
        # For v3.0, we scan on demand to ensure accuracy.
        self.scan_screen()
        
        target_clean = target_text.lower().strip()
        
        with self.lock:
            # Exact match attempt
            for item in self.screen_map:
                if item["text"] == target_clean:
                    return {"x": item["x"], "y": item["y"]}
            
            # Fuzzy/Partial match attempt
            for item in self.screen_map:
                if target_clean in item["text"]:
                    return {"x": item["x"], "y": item["y"]}
                    
        return None