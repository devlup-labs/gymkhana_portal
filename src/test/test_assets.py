import random
import tempfile
from django.conf import settings
from PIL import Image
from django.utils import timezone

TEST_TEMPLATES = settings.TEMPLATES
TEST_TEMPLATES[0]['DIRS'].append(tempfile.gettempdir())
TEST_MEDIA_ROOT = tempfile.gettempdir()


def get_temporary_image():
    temp_image_file = tempfile.NamedTemporaryFile()
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_image_file, 'jpeg')
    return temp_image_file


def get_temporary_html():
    temp_html_file = tempfile.NamedTemporaryFile()
    with open(temp_html_file.name, "w") as f:
        f.write("{% extends 'main/base.html' %}")
    f.close()
    return temp_html_file


def get_random_date(now=False):
    year = random.randint(1980, timezone.now().year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return timezone.datetime(year=year, month=month, day=day,
                             tzinfo=timezone.now().tzinfo) if not now else timezone.now()
