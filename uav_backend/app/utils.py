import numpy as np
import cv2

def generate_noisy_image():
    noisy_image = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    is_success, buffer = cv2.imencode('.jpg', noisy_image)
    return buffer.tobytes()
