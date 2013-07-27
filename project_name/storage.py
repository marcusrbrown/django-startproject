from django.contrib.staticfiles.storage import CachedFilesMixin
from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class UrlCorrectedS3BotoStorage(S3BotoStorage):
    """
    Overrides the url() method to readd a trailing slash if it was removed by
    the base class.
    """

    def url(self, name):
        url = super(UrlCorrectedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, UrlCorrectedS3BotoStorage):
    pass


# Specifies storage for uploaded files (media files).
# From http://stackoverflow.com/a/10825691/904847
#MediaS3BotoStorage = lambda: UrlCorrectedS3BotoStorage(location='media')
class MediaS3BotoStorage(UrlCorrectedS3BotoStorage):
    """Provides storage for uploaded files."""
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(MediaS3BotoStorage, self).__init__(*args, **kwargs)
