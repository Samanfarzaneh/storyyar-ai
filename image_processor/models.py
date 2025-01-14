from django.db import models

from django.db import models

class UploadedImage(models.Model):
    source_image = models.ImageField(upload_to='media/image_processor/source_images/')
    target_image = models.ImageField(upload_to='media/image_processor/target_images/')
    output_image = models.ImageField(upload_to='media/image_processor/enhanced_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - Source and Target"

    def get_source_image_url(self):

        return self.source_image.url if self.source_image else None

    def get_target_image_url(self):

        return self.target_image.url if self.target_image else None

    def get_output_image_url(self):

        return self.output_image.url if self.output_image else None


class ImageProcessing(models.Model):
    image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='processing')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Processing {self.id} - {self.status}"
