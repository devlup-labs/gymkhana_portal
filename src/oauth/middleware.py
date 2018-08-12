from django.shortcuts import HttpResponseRedirect, reverse


class UserProfileExistsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not hasattr(request.user, 'userprofile') and request.user.is_authenticated and not request.path == reverse(
                'oauth:register') and 'admin' not in request.path:
            return HttpResponseRedirect(reverse('oauth:register'))
        return response
