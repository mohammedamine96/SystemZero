import cv2
import numpy as np
import pyautogui
import easyocr
import time

def run_diagnostics():
    print(">> [DIAGNOSTIC] Initializing Vision System (this may take time on first run)...")
    
    # Initialize Reader
    try:
        reader = easyocr.Reader(['en'], gpu=True) # Set gpu=False if you don't have NVIDIA
        print(">> [DIAGNOSTIC] Vision Model Loaded.")
    except Exception as e:
        print(f">> [CRITICAL FAIL] Could not load EasyOCR: {e}")
        return

    print(">> [DIAGNOSTIC] Capturing screen in 3 seconds. Open a window with text!")
    time.sleep(3)

    # 1. Capture
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 2. Process
    print(">> [DIAGNOSTIC] Scanning...")
    start_time = time.time()
    results = reader.readtext(image)
    end_time = time.time()
    
    print(f">> [DIAGNOSTIC] Scan complete in {end_time - start_time:.2f}s")
    print(f">> [DIAGNOSTIC] Found {len(results)} text elements.")

    # 3. Visualize
    for (bbox, text, prob) in results:
        # Define corner points
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        br = (int(br[0]), int(br[1]))

        # Draw rectangle and text
        cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Print to console for verification
        print(f"   - Detected: '{text}' (Confidence: {prob:.2f})")

    # 4. Save Output
    output_filename = "vision_diagnostic_result.png"
    cv2.imwrite(output_filename, image)
    print(f">> [SUCCESS] Diagnostic image saved to {output_filename}")
    print(">> Inspect this image to ensure text is being read correctly.")

if __name__ == "__main__":
    run_diagnostics()