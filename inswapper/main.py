from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

from image_processor.models import UploadedImage, ImageProcessing
from .swapper import *
from PIL import Image
from codeformer.app import inference_app, imwrite
import os


def process_and_enhance_image(source_image, target_image, image_id):
    image_id = int(image_id)
    model = "./checkpoints/inswapper_128.onnx"

    # باز کردن تصاویر به صورت صحیح
    try:
        source_img = Image.open(source_image).convert("RGB")  # تبدیل به RGB اگر نیاز باشد
        target_img = Image.open(target_image).convert("RGB")
    except Exception as e:
        print(f"Error opening images: {e}")
        return None  # بازگشت None در صورت بروز خطا در بارگذاری تصاویر

    # انجام تغییر چهره
    try:
        face_swap_result = process([source_img], target_img, "0", "0", model)
    except Exception as e:
        print(f"Face swap error: {e}")
        return None  # بازگشت None در صورت بروز خطا در پردازش تغییر چهره

    # ذخیره تصویر تغییر چهره
    face_swap_result_path = os.path.join(settings.MEDIA_ROOT, f"image_processor/cach/face_swap_result/result_{image_id}.png")
    face_swap_result.save(face_swap_result_path)

    print("تغییر چهره انجام شد و تصویر ذخیره شد در:", face_swap_result_path)

    # افزایش کیفیت تصویر
    try:
        enhanced_img = inference_app(
            image=face_swap_result_path,
            face_upsample=False,
            background_enhance=True,
            upscale=2,
            codeformer_fidelity=0.7,
        )
    except Exception as e:
        print(f"Enhancement error: {e}")
        return False  # بازگشت None در صورت بروز خطا در پردازش افزایش کیفیت

    # مسیر ذخیره تصاویر پردازش شده
    enhanced_images_dir = os.path.join(settings.MEDIA_ROOT, 'image_processor', 'enhanced_images')
    os.makedirs(enhanced_images_dir, exist_ok=True)

    # ذخیره تصویر با کیفیت بالاتر در پوشه enhanced_images
    output_path = os.path.join(enhanced_images_dir, f"enhanced_result_{image_id}.png")
    imwrite(enhanced_img, str(output_path))
    print(f"کیفیت تصویر افزایش یافت و خروجی ذخیره شد در: {output_path}")

    return True
