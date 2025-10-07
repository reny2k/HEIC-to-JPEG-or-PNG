import os
from PIL import Image
from pillow_heif import register_heif_opener
import cv2
import mediapipe as mp
import numpy as np

# Register HEIC support
register_heif_opener()

# Input and output folders
input_folder = r"C:\your\folder\path" #
output_folder = r"C:\your\folder\path"
os.makedirs(output_folder, exist_ok=True)

# Mediapipe setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

def extract_body(image_path, output_path): #Remove this section if you just want to convert photo as is
    image = Image.open(image_path).convert("RGB")
    np_img = np.array(image)
    results = pose.process(cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR))

    if results.pose_landmarks:
        # Get bounding box from landmarks
        landmarks = results.pose_landmarks.landmark
        xs = [lm.x * image.width for lm in landmarks]
        ys = [lm.y * image.height for lm in landmarks]
        x_min, x_max = int(min(xs)), int(max(xs))
        y_min, y_max = int(min(ys)), int(max(ys))

        # Add padding
        pad = 20
        x_min = max(x_min - pad, 0)
        x_max = min(x_max + pad, image.width)
        y_min = max(y_min - pad, 0)
        y_max = min(y_max + pad, image.height)

        # Crop and save as JPEG
        cropped = image.crop((x_min, y_min, x_max, y_max))
        cropped.save(output_path, format="JPEG", quality=95)
        print(f"✅ Saved: {output_path}")
    else:
        print(f"❌ No body detected in: {image_path}") #End of code that strips body only

# Process all HEIC files
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".heic"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + "_body.jpeg"
        output_path = os.path.join(output_folder, output_filename)
        extract_body(input_path, output_path)