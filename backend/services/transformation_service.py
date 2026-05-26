import io
import numpy as np
from PIL import Image as PillowImage, ImageDraw, ImageFont

class TransformationService:

    def apply(self, image, params):
        output_format = image.format or 'JPEG'
        
        if 'resize' in params:
            width = params['resize']['width']
            height = params['resize']['height']
            image = image.resize((width, height))
        
        if 'crop' in params:
            left = params['crop']['x']
            upper = params['crop']['y']
            right = (params['crop']['x'] + params['crop']['width'])
            lower = (params['crop']['y'] + params['crop']['height'])
            image = image.crop((left, upper, right, lower))
        
        if 'rotate' in params and params['rotate']:
            image = image.rotate(params['rotate'], expand=True)

        if 'flip' in params and params['flip']:
            image = image.transpose(PillowImage.FLIP_TOP_BOTTOM)

        if 'mirror' in params and params['mirror']:
            image = image.transpose(PillowImage.FLIP_LEFT_RIGHT)

        if 'filters' in params:
            if params['filters'].get('grayscale'):
                image = image.convert('L').convert('RGB')
            
            if params['filters'].get('sepia'):
                image = image.convert('RGB')
                img_array = np.array(image, dtype=np.float64)
                sepia_filter = np.array([
                    [0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]
                ])
                sepia_array = img_array @ sepia_filter.T
                sepia_array = np.clip(sepia_array, 0, 255).astype(np.uint8)
                image = PillowImage.fromarray(sepia_array)

        if 'watermark' in params:
            image = image.convert('RGBA')
            draw = ImageDraw.Draw(image)
            text = params['watermark']
            try:
                font = ImageFont.truetype('arial.ttf', 36)
            except IOError:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            margin = 10
            x = image.width - text_width - margin
            y = image.height - text_height - margin
            draw.text((x, y), text, fill=(255, 255, 255, 180), font=font)
            image = image.convert('RGB')

        if 'compress' in params:
            output_format = 'JPEG'
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=params['compress'])
            buffer.seek(0)
            image = PillowImage.open(buffer)

        if 'format' in params and params['format']:
            output_format = params['format'].upper()
            if output_format == 'JPG':
                output_format = 'JPEG'

        return image, output_format
    
transformation_service = TransformationService()