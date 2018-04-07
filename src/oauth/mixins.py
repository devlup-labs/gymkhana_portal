from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin


class SocialLinkOwnerMixin(LoginRequiredMixin, SingleObjectMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id is not self.get_object().user.id:
            raise PermissionDenied
        return super(SocialLinkOwnerMixin, self).dispatch(request, *args, **kwargs)
