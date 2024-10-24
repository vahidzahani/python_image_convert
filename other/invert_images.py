import os
from PIL import Image, ImageOps

def invert_images_in_folder(folder_path='.'):
    # پیمایش تمام فایل‌ها و پوشه‌های موجود
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # بررسی اینکه آیا فایل فرمت jpg یا png دارد
            if file.lower().endswith(('.jpg', '.png')):
                file_path = os.path.join(root, file)
                try:
                    # باز کردن تصویر
                    with Image.open(file_path) as img:
                        # اینورت کردن تصویر
                        inverted_image = ImageOps.invert(img.convert('RGB'))
                        # ذخیره تصویر اینورت شده به همان نام
                        inverted_image.save(file_path)
                        print(f"Inverted and saved: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# فراخوانی تابع برای پوشه فعلی و زیرپوشه‌ها
invert_images_in_folder()
