from django.http import HttpResponse
from django.conf import settings


class MaintenanceMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if settings.MAINTENANCE_MODE:
            return HttpResponse("We're currently under maintenance, please visit again.", status=503)
        else:
            return super().dispatch(request, args, kwargs)
