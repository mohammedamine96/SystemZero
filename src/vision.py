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
        self.screen_map = [] 
        self.lock = threading.Lock()
        print(">> [EYES] Vision Module Online.")

    def scan_screen(self):
        print(">> [EYES] Scanning current visual field...")
        
        # 1. Capture Full Screen
        screenshot = pyautogui.screenshot()
        image = np.array(screenshot)
        
        # --- SAFE OPTIMIZATION ---
        # Convert to Grayscale instead of resizing. 
        # This makes OCR faster without destroying text resolution!
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 2. Read Text (Pass the FULL RESOLUTION grayscale image)
        results = self.reader.readtext(gray_image)
        
        # 3. Update Spatial Map (1:1 Coordinates)
        new_map = []
        for (bbox, text, prob) in results:
            # Lowered probability threshold slightly to catch thin UI fonts
            if prob > 0.3: 
                # Calculate the center of the bounding box
                center_x = int((bbox[0][0] + bbox[2][0]) / 2)
                center_y = int((bbox[0][1] + bbox[2][1]) / 2)
                
                new_map.append({
                    "text": text.lower().strip(),
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
        self.scan_screen()
        
        target_clean = target_text.lower().strip()
        
        with self.lock:
            # Exact match attempt
            for item in self.screen_map:
                if item["text"] == target_clean:
                    return {"x": item["x"], "y": item["y"]}
            
            # Fuzzy/Partial match attempt
            for item in self.screen_map:
                if target_clean in item["text"] or item["text"] in target_clean:
                    return {"x": item["x"], "y": item["y"]}
                    
        return None