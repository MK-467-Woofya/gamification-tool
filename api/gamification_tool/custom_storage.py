from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Class defining static storage Location for boto3"""
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'
    querystring_auth = False


class MediaStorage(S3Boto3Storage):
    """Class defining media storage Location for boto3"""
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
