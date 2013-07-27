import os
from pipeline.storage import PipelineFinderStorage

# Replaces the match_location() method in PipelineFinderStorage to normalize
# the file name passed into the method. This fixes an issue where
# django-pipeline can't locate files on Windows - the storage path is in
# Windows format, but the name isn't.
# TODO: Find a concise solution and submit it to djange-pipeline upstream.
class PipelineFinderStorageCorrected(PipelineFinderStorage):
    def match_location(self, name, path, prefix=None):
        name = os.path.normpath(name)
        return super(PipelineFinderStorageCorrected, self).match_location(name, path, prefix)
