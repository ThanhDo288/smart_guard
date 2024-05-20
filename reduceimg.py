import os
from PIL import Image

def compress_images_in_folder(source_folder, target_folder, max_size=(1080, 720), quality=75):
    """
    Compress all JPEG images in the source folder and save them to the target folder with reduced file size.
    
    Args:
    - source_folder: Directory containing the original images.
    - target_folder: Directory where the compressed images will be saved.
    - max_size: Maximum size of the images as a tuple (width, height).
    - quality: Quality of the saved images (1 to 100).
    """
    # Ensure target directory exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Loop through all files in the source directory
    for filename in os.listdir(source_folder):
        if filename.lower().endswith('.jpg'):
            # Construct file paths
            original_path = os.path.join(source_folder, filename)
            compressed_path = os.path.join(target_folder, filename)
            
            # Open and compress the image
            with Image.open(original_path) as img:
                img.thumbnail(max_size, Image.ANTIALIAS)
                img.save(compressed_path, 'JPEG', quality=quality, optimize=True)
                
            print(f"Compressed image saved at {compressed_path}")

# Example usage
source_dir = '/home/thanhdo/iot/AIfile/train'
target_dir = '/home/thanhdo/iot/AIfile/train2'
compress_images_in_folder(source_dir, target_dir)
