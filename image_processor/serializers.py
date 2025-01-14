from rest_framework import serializers
from .models import UploadedImage, ImageProcessing

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'source_image', 'target_image', 'output_image', 'created_at']

class ImageProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProcessing
        fields = ['id', 'image', 'status', 'started_at', 'completed_at', 'error_message']
