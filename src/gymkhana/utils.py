from collections import OrderedDict
from os.path import exists

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
from django.contrib.staticfiles.utils import get_files
from django.core.checks import Error
from django.core.files.storage import FileSystemStorage
from versatileimagefield.utils import build_versatileimagefield_url_set, get_rendition_key_set

from gallery.schema import RenditionType


def build_image_types(request, image, key_set):
    data = []
    for key, value in build_versatileimagefield_url_set(image, get_rendition_key_set(key_set), request=request).items():
        data.append(RenditionType(name=key, url=value))
    return data


searched_locations = []


class VueFilesFinder(FileSystemFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = OrderedDict()
        for root in settings.VUE_DIRS:
            if isinstance(root, (list, tuple)):
                prefix, root = root
            else:
                prefix = ''
            if (prefix, root) not in self.locations:
                self.locations.append((prefix, root))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage

    def check(self, **kwargs):
        errors = []
        if not exists(settings.VUE_ROOT):
            errors.append(Error(
                'The VUE_ROOT doesn\'t exist.',
                hint=f'Make sure the dir {settings.VUE_ROOT} exists',
                id='vue.E001',
            ))
        return errors

    def list(self, ignore_patterns):
        for prefix, root in self.locations:
            if exists(root):
                storage = self.storages[root]
                for path in get_files(storage, ignore_patterns):
                    yield path, storage
