import argparse
from docx import Document
from PIL import Image, ImageOps
import os

def extract_and_invert_images_from_docx(docx_path, output_docx_path):
    # مرحله 1: باز کردن فایل docx
    doc = Document(docx_path)
    
    # مرحله 2: ساخت پوشه موقت برای ذخیره تصاویر
    images_folder = 'extracted_images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    image_count = 0
    image_mapping = {}

    # مرحله 3: جستجوی تصاویر در فایل docx
    for rel in doc.part.rels:
        if "image" in doc.part.rels[rel].target_ref:
            image_count += 1
            image_part = doc.part.rels[rel].target_part
            image_data = image_part.blob

            # استخراج تصویر
            image_file_path = os.path.join(images_folder, f"image_{image_count}.png")
            with open(image_file_path, 'wb') as f:
                f.write(image_data)

            # اینورت کردن تصویر
            try:
                with Image.open(image_file_path) as img:
                    inverted_img = ImageOps.invert(img.convert('RGB'))
                    inverted_img.save(image_file_path)
                    print(f"Inverted image saved: {image_file_path}")

                    # نگه داشتن نقشه تصویر برای جایگزینی بعدی
                    image_mapping[rel] = image_file_path
            except Exception as e:
                print(f"Error inverting image {image_file_path}: {e}")

    if image_count == 0:
        print("No images found in the document.")
        return
    
    # مرحله 4: جایگزینی تصاویر در سند docx
    for rel in image_mapping:
        image_file_path = image_mapping[rel]

        # باز کردن تصویر اینورت شده
        with open(image_file_path, 'rb') as f:
            new_image_data = f.read()

        # به‌روزرسانی داده‌های تصویر در سند
        doc.part.rels[rel].target_part._blob = new_image_data

    # مرحله 5: ذخیره فایل docx جدید
    doc.save(output_docx_path)
    print(f"Output docx saved as '{output_docx_path}'")

# استفاده از argparse برای دریافت ورودی از کاربر
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract and invert images from a Word document.")
    parser.add_argument("input_docx", help="Path to the input .docx file")
    parser.add_argument("--out", default="output.docx", help="Path to save the output .docx file (default: output.docx)")

    args = parser.parse_args()

    # فراخوانی تابع برای فایل‌های ورودی و خروجی
    extract_and_invert_images_from_docx(args.input_docx, args.out)
