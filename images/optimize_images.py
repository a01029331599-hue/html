import os
from PIL import Image

def optimize_image(file_path, output_dir, max_width=1200, quality=85):
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    try:
        img = Image.open(file_path)
    except Exception as e:
        print(f"Error opening {filename}: {e}")
        return
        
    # Resize if wider than max_width
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        new_w = int(max_width)
        new_h = int(h * ratio)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        print(f"Resized {filename}: {w}x{h} -> {new_w}x{new_h}")
        
    # Determine target format and path
    # Convert certifications and brochures to JPG if possible, or keep PNG for sharp text.
    # Actually, JPEGs are much smaller, and for photos (factory) it's definitely JPG.
    if ext == '.bmp' or 'factory' in name:
        target_ext = '.jpg'
        target_format = 'JPEG'
    elif 'brochure' in name:
        target_ext = '.jpg'
        target_format = 'JPEG'
    else:
        # Keep certificates as PNG, but save with optimization
        target_ext = '.png'
        target_format = 'PNG'
        
    # Handle transparency when converting to JPG
    if target_format == 'JPEG' and img.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        img = background
    elif target_format == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')
        
    new_filename = f"{name}{target_ext}"
    dest_path = os.path.join(output_dir, new_filename)
    
    try:
        if target_format == 'JPEG':
            img.save(dest_path, format=target_format, quality=quality, optimize=True)
        else:
            img.save(dest_path, format=target_format, optimize=True)
            
        orig_size = os.path.getsize(file_path)
        new_size = os.path.getsize(dest_path)
        print(f"Saved: {new_filename} ({orig_size/1024:.1f}KB -> {new_size/1024:.1f}KB, -{(1 - new_size/orig_size)*100:.1f}%)")
        
        # Remove original if filename/ext changed
        if file_path != dest_path:
            os.remove(file_path)
            
    except Exception as e:
        print(f"Error saving {new_filename}: {e}")

def main():
    workspace_dir = r"c:\Users\82102\OneDrive\바탕 화면\anti"
    images_dir = os.path.join(workspace_dir, "images")
    
    if not os.path.exists(images_dir):
        print(f"Images directory not found: {images_dir}")
        return
        
    for filename in os.listdir(images_dir):
        file_path = os.path.join(images_dir, filename)
        if not os.path.isfile(file_path):
            continue
            
        ext = os.path.splitext(filename)[1].lower()
        if ext in ('.bmp', '.png', '.jpg', '.jpeg'):
            # Ignore already optimized jpg unless they are BMP/PNG to be converted
            if ext == '.jpg' and not filename.startswith('factory'):
                continue
            optimize_image(file_path, images_dir)

if __name__ == "__main__":
    main()
