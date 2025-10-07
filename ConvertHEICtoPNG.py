from pillow_heif import register_heif_opener
from PIL import Image
import os

# Register HEIF support
register_heif_opener()

# Set your input and output folders
input_folder = r"C:\your\folder\here"
output_folder = os.path.join(input_folder, "converted_pngs")
os.makedirs(output_folder, exist_ok=True)

# Loop through HEIC files and convert to PNG
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".heic"):
        heic_path = os.path.join(input_folder, filename)
        png_filename = os.path.splitext(filename)[0] + ".png"
        png_path = os.path.join(output_folder, png_filename)

        try:
            image = Image.open(heic_path)
            image.save(png_path, format="PNG")
            print(f"✅ Converted: {filename} → {png_filename}")
        except Exception as e:
            print(f"❌ Failed to convert {filename}: {e}")