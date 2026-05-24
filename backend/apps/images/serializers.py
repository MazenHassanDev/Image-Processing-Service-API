from .models import Image, ImageTransformation
from rest_framework import serializers
from PIL import Image as PillowImage
from services.storage_service import storage_service


class ImageUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()


    def validate_file(self, file):
        if file.size > 10 * 1024 * 1024:
            raise serializers.ValidationError({'error': 'File too big.'})
        
        allowed_formats = ['JPEG', 'PNG', 'WEBP', 'GIF', 'BMP', 'TIFF']
        
        try:
            img = PillowImage.open(file)
            img.verify()
            file.seek(0)
        except Exception:
            raise serializers.ValidationError({'error': 'File is not a valid image.'})
        
        img = PillowImage.open(file)
        if img.format not in allowed_formats:
            raise serializers.ValidationError({'error': f"Unsupported format. Allowed: {', '.join(allowed_formats)}"})
        file.seek(0)

        return file
    
class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'original_filename', 'url', 'file_size', 'width', 'height', 'format_image', 'uploaded_at']

    def get_url(self, obj):
        return storage_service.get_url(obj.file)

class ImageTransformationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = ImageTransformation
        fields = ['id', 'original_image', 'transformation_params', 'url', 'width', 'height', 'format_image', 'created_at']

    def get_url(self, obj):
        return storage_service.get_url(obj.file)
