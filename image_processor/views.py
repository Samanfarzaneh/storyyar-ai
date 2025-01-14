import json
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from inswapper.main import process_and_enhance_image
from rest_framework.response import Response


def upload_image(request):
    """
    ویو نمایش فرم آپلود تصاویر
    """
    if request.method == 'POST':
        return render(request, 'upload_image/upload_images.html')
    return render(request, 'upload_image/upload_images.html')


def process_upload_images(request):
    """
    ویوی نمایش فرم آپلود تصاویر و پردازش آن‌ها
    """
    if request.method == 'POST' and request.FILES.get('source') and request.FILES.get('target'):
        source_image = request.FILES['source']
        target_image = request.FILES['target']

        # ابتدا رکورد UploadedImage را ذخیره کنید
        uploaded_image = UploadedImage.objects.create(
            source_image='',
            target_image='',
            output_image='',
        )

        # استفاده از FileSystemStorage برای ذخیره تصاویر
        source_image_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'image_processor/source_images'))
        target_image_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'image_processor/target_images'))

        # استخراج پسوند فایل‌ها
        source_image_extension = os.path.splitext(source_image.name)[1]  # .jpg یا .png
        target_image_extension = os.path.splitext(target_image.name)[1]  # .jpg یا .png

        # ذخیره فایل‌ها در پوشه‌های مشخص با نام فایل شامل PK و پسوند
        source_image_name = f"SOURCE_IMAGE_{uploaded_image.id}{source_image_extension}"
        target_image_name = f"TARGET_IMAGE_{uploaded_image.id}{target_image_extension}"

        # ذخیره تصاویر
        source_image_storage.save(source_image_name, source_image)
        target_image_storage.save(target_image_name, target_image)

        # به‌روزرسانی مسیر فایل‌ها در رکورد
        uploaded_image.source_image = f'image_processor/source_images/{source_image_name}'
        uploaded_image.target_image = f'image_processor/target_images/{target_image_name}'
        uploaded_image.save()  # ذخیره رکورد با مسیرهای به‌روزرسانی شده

        # پردازش تصویر (در صورت نیاز به پردازش)
        source_image_path = os.path.join(source_image_storage.location, source_image_name)
        target_image_path = os.path.join(target_image_storage.location, target_image_name)

        final_output_path = process_and_enhance_image(source_image_path, target_image_path, uploaded_image.id)
        print(final_output_path)

        # در صورتی که پردازش موفقیت‌آمیز بود
        if final_output_path:
            uploaded_image.output_image = f'image_processor/enhanced_images/enhanced_result_{uploaded_image.id}.png'
            uploaded_image.save()  # ذخیره مسیر خروجی

            # به API نمایش نتیجه هدایت می‌کنیم
            return redirect(reverse('show_result_by_api', args=[uploaded_image.id]))
        elif final_output_path is None:
            return render(request, 'errors/no_face_detected.html')
        else:
            return render(request, 'errors/500-error.html')


    return render(request, 'upload_image/upload_images.html')


@api_view(['GET'])
def show_result_by_api(request, pk):
    try:
        # تلاش برای یافتن رکورد با pk مشخص
        image = UploadedImage.objects.get(pk=pk)

        # سریالایز کردن داده‌ها
        serializer = UploadedImageSerializer(image)
        print(serializer.data)

        # داده‌ها را به قالب HTML ارسال می‌کنیم
        return render(request, 'show_result/show_result.html', {'image_path': serializer.data})

    except UploadedImage.DoesNotExist:
        # در صورتی که رکورد با pk مورد نظر یافت نشد
        return render(request, 'show_result/show_result.html', {'error_message': 'تصویر با این شناسه پیدا نشد.'})

    except Exception as e:
        # در صورتی که خطای دیگری رخ دهد
        return render(request, 'show_result/show_result.html', {'error_message': str(e)})


@csrf_exempt
def sample_api(request):
    if request.method == 'POST':
        try:
            # دریافت داده‌های ارسالی در قالب JSON
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name', 'Guest')
            message = data.get('message', 'No message provided.')

            # پاسخ به درخواست
            response = {
                "status": "success",
                "received_name": name,
                "received_message": message,
            }
            return JsonResponse(response, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"message": "Send a POST request to use this API."}, status=200)




class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    @action(detail=True, methods=['get'])
    def custom_action(self, request, pk=None):
        uploaded_image = self.get_object()
        # Custom logic for specific image actions
        return Response({'message': 'Custom action executed', 'uploaded_image': uploaded_image.id})




@csrf_exempt
@api_view(['POST'])
def process_images_api(request):
    if request.method == 'POST' and request.FILES.get('source') and request.FILES.get('target'):
        try:
            source_image = request.FILES['source']
            target_image = request.FILES['target']

            # ذخیره رکورد اولیه
            uploaded_image = UploadedImage.objects.create(
                source_image='',
                target_image='',
                output_image='',
            )

            # ایجاد مسیر ذخیره تصاویر
            source_image_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'image_processor/source_images'))
            target_image_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'image_processor/target_images'))

            # استخراج پسوند فایل‌ها
            source_image_extension = os.path.splitext(source_image.name)[1]
            target_image_extension = os.path.splitext(target_image.name)[1]

            # ساخت نام فایل‌ها
            source_image_name = f"SOURCE_IMAGE_{uploaded_image.id}{source_image_extension}"
            target_image_name = f"TARGET_IMAGE_{uploaded_image.id}{target_image_extension}"

            # ذخیره تصاویر
            source_image_storage.save(source_image_name, source_image)
            target_image_storage.save(target_image_name, target_image)

            # به‌روزرسانی مسیر فایل‌ها در رکورد
            uploaded_image.source_image = f'image_processor/source_images/{source_image_name}'
            uploaded_image.target_image = f'image_processor/target_images/{target_image_name}'
            uploaded_image.save()

            # مسیر کامل تصاویر
            source_image_path = os.path.join(source_image_storage.location, source_image_name)
            target_image_path = os.path.join(target_image_storage.location, target_image_name)

            # پردازش تصویر
            final_output_path = process_and_enhance_image(source_image_path, target_image_path, uploaded_image.id)

            if final_output_path:
                # به‌روزرسانی مسیر خروجی در دیتابیس
                uploaded_image.output_image = f'image_processor/enhanced_images/enhanced_result_{uploaded_image.id}.png'
                uploaded_image.save()

                # بازگشت پاسخ موفقیت و هدایت به نمایش نتیجه
                return JsonResponse({
                    'status': 'success',
                    'output_image': f'{settings.MEDIA_URL}{uploaded_image.output_image}'
                }, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'پردازش تصویر با خطا مواجه شد.'}, status=500)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400)


