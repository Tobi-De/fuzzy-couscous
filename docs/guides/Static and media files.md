


## Media storage

Media files in django usually refer to files uploaded by users, profile pictures, product images, etc.
I usually manage my media files using [django-storages](https://github.com/jschneier/django-storages).
Here is how I set it up.

```python
# core/storages.py
from storages.backends.s3boto3 import S3Boto3Storage

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


# settings.py - production settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "project_name.core.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"
```