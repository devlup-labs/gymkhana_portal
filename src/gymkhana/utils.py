from versatileimagefield.utils import build_versatileimagefield_url_set, validate_versatileimagefield_sizekey_list, \
    get_rendition_key_set

from main.schema import RenditionType


def build_image_types(request, image, key_set):
    data = []
    for key, value in build_versatileimagefield_url_set(image, validate_versatileimagefield_sizekey_list(
            get_rendition_key_set(key_set)), request=request).items():
        data.append(RenditionType(name=key, url=value))
    return data
