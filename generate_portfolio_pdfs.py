#!/usr/bin/env python3
import os
import glob
from PIL import Image

def create_pdf(image_paths, output_path):
    if not image_paths:
        return
    
    images = []
    print(f"Creating {output_path} with {len(image_paths)} images...")
    
    for path in image_paths:
        try:
            img = Image.open(path).convert('RGB')
            images.append(img)
        except Exception as e:
            print(f"Error loading {path}: {e}")

    if images:
        images[0].save(
            output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:], optimize=True
        )
        print(f"Saved: {output_path}")

def main():
    base_dir = "screenshots"
    out_dir = "pdfs"
    os.makedirs(out_dir, exist_ok=True)

    # Get all screenshots sorted by name (01-..., 02-...)
    all_images = sorted(glob.glob(f"{base_dir}/*.png"))
    
    if not all_images:
        print("No images found!")
        return

    # Filter for specific PDFs
    admin_images = [img for img in all_images if "admin" in img]
    student_images = [img for img in all_images if "student" in img]
    
    # 1. Complete Showcase (All)
    create_pdf(all_images, f"{out_dir}/complete-showcase.pdf")
    
    # 2. Key Features (All - or subset if preferred, using All for now)
    create_pdf(all_images, f"{out_dir}/key-features.pdf")

    # 3. Admin Features
    create_pdf(admin_images, f"{out_dir}/admin-features.pdf")

    # 4. Student Features
    create_pdf(student_images, f"{out_dir}/student-features.pdf")

if __name__ == "__main__":
    main()
