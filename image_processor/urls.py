# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UploadedImageViewSet, upload_image, process_upload_images, sample_api, process_images_api
from django.conf import settings
from django.conf.urls.static import static

# تنظیم روت‌های API با استفاده از DefaultRouter
router = DefaultRouter()
router.register(r'uploaded-images', UploadedImageViewSet)

urlpatterns = [
    path('', upload_image, name='upload_image'),
    path('process_image/', process_upload_images, name='process_image'),
    path('api/result/<int:pk>/', views.show_result_by_api, name='show_result_by_api'),
    path('sample-api/', sample_api, name='sample_api'),
    path('api/process-images/', process_images_api, name='process_images_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
