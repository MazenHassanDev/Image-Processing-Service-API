from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    class Meta:
        ordering = ['-uploaded_at']

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images')
    original_filename = models.CharField(max_length=250)
    file = models.CharField(max_length=500)
    file_size = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    format_image = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ImageTransformation(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        COMPLETE = 'complete'
        FAILED = 'failed'

    class Meta:
        ordering = ['-created_at']

    original_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='transformations')
    transformation_params = models.JSONField()
    file = models.CharField(max_length=500)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    format_image = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)