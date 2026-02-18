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
        print(">> [EYES] Scanning current visual field...")
        
        # 1. Capture
        screenshot = pyautogui.screenshot()
        image = np.array(screenshot)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # --- NEW OPTIMIZATION START ---
        # Resize image to 50% scale to speed up processing
        # This reduces pixel count by 75%, making OCR much faster
        scale_ratio = 0.5 
        width = int(image.shape[1] * scale_ratio)
        height = int(image.shape[0] * scale_ratio)
        small_image = cv2.resize(image, (width, height))
        # --- NEW OPTIMIZATION END ---
        
        # 2. Read Text (Pass the small image!)
        results = self.reader.readtext(small_image)
        
        # 3. Update Spatial Map (We must scale coordinates BACK up)
        new_map = []
        for (bbox, text, prob) in results:
            if prob > 0.4: 
                # Map coordinates back to original screen size
                # by dividing by scale_ratio
                top_left = [int(bbox[0][0] / scale_ratio), int(bbox[0][1] / scale_ratio)]
                bottom_right = [int(bbox[2][0] / scale_ratio), int(bbox[2][1] / scale_ratio)]
                
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                
                new_map.append({
                    "text": text.lower(),
                    "x": center_x,
                    "y": center_y
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