from django.core.exceptions import ValidationError

def allow_only_images_validators(value):
    import os
    ext = os.path.splitext(value.name)[1]  
    valid_extensions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: '+ str(valid_extensions))