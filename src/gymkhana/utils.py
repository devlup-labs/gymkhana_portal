from versatileimagefield.utils import build_versatileimagefield_url_set, get_rendition_key_set

from gallery.schema import RenditionType


def build_image_types(request, image, key_set):
    data = []
    for key, value in build_versatileimagefield_url_set(image, get_rendition_key_set(key_set), request=request).items():
        data.append(RenditionType(name=key, url=value))
    return data
