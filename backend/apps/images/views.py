
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageUploadSerializer, ImageSerializer, ImageTransformationSerializer
from .models import Image, ImageTransformation
from services.storage_service import storage_service
from PIL import Image as PillowImage
from django.shortcuts import get_object_or_404
from django.core.cache import cache


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_image(request):
    if request.method == 'GET':
        qs = Image.objects.filter(owner=request.user)
        serializer = ImageSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_file = serializer.validated_data['file']

            img = PillowImage.open(user_file)
            width = img.width
            height = img.height
            img_format = img.format
            user_file.seek(0)

            key = storage_service.save(
                file=user_file, 
                filename=user_file.name, 
                user_id=request.user.id
                )

            image = Image.objects.create(
                owner = request.user,
                original_filename= user_file.name,
                file=key,
                file_size= user_file.size,
                width= width,
                height= height,
                format_image = img_format,
                
            )
            outputImage = ImageSerializer(image)
            return Response(outputImage.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def image_detail(request, pk):
    cache_key = f"image:{pk}:url"

    if request.method == 'GET':
        cached = cache.get(cache_key)

        if cached:
            response = Response(cached, status=status.HTTP_200_OK)
            response['X-Cache'] = 'HIT'
            return response
        
        image = get_object_or_404(Image, pk=pk, owner=request.user)
        serializer = ImageSerializer(image)
        cache.set(cache_key, serializer.data, timeout=60*60)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        response['X-Cache'] = 'MISS'
        return response


    if request.method == 'DELETE':
        image = get_object_or_404(Image, pk=pk, owner=request.user)
        transformations = image.transformations.all()
        for transform in transformations:
            storage_service.delete(transform.file)
        
        storage_service.delete(image.file)
        
        image.delete()
        cache.delete(cache_key)
        return Response({'message': 'Image deleted.'}, status=status.HTTP_200_OK)