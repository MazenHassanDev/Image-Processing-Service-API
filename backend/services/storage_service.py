import os
import io
import boto3
import uuid
from django.conf import settings

class StorageService:
    def _generate_key(self, filename, user_id, folder):
        extension = filename.rsplit('.', 1)[-1].lower()
        key = f"{folder}/{user_id}/{uuid.uuid4()}.{extension}"
        return key
    
    def _get_s3_client(self):
        return boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                region_name = settings.AWS_S3_REGION_NAME
            )

    def save(self, file, filename, user_id, folder='uploads'):
        key = self._generate_key(filename=filename, user_id=user_id, folder=folder)
        
        if settings.USE_S3:
            s3 = self._get_s3_client()
            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, key)
        else:
            path = os.path.join(settings.MEDIA_ROOT, key)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        
        return key

    def get_url(self, key):
        if settings.USE_S3:
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
        else:
            return f"http://localhost:8000{settings.MEDIA_URL}{key}"

    def get_file(self, key):
        if settings.USE_S3:
            s3 = self._get_s3_client()
            response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            file_bytes = response['Body'].read()
            buffer = io.BytesIO(file_bytes)
            buffer.seek(0)
            return buffer
        else:
            path = os.path.join(settings.MEDIA_ROOT, key)
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {key}")
            
            with open(path, 'rb') as file:
                file_bytes = file.read()
                
            buffer = io.BytesIO(file_bytes)
            buffer.seek(0)
            return buffer
        

    def delete(self, key):
        if settings.USE_S3:
            s3 = self._get_s3_client()
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        else:
            path = os.path.join(settings.MEDIA_ROOT, key)
            if os.path.exists(path):
                os.remove(path)

storage_service = StorageService()
