from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect, reverse
from rest_framework.views import APIView
from .mixins import SocialLinkOwnerMixin
from .models import UserProfile, SocialLink
from .forms import UserProfileUpdateForm, SocialLinkForm, UserProfileForm
from django.urls import reverse_lazy


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'oauth/profile_detail.html'

    def get_object(self, queryset=None):
        roll = self.kwargs.get('roll')
        return get_object_or_404(UserProfile, roll=roll.upper(), email_confirmed=True)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['social_media_count'] = len(SocialLink.SM_CHOICES)
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'oauth/profile_edit.html'
    form_class = UserProfileUpdateForm

    def get_object(self, queryset=None):
        roll = self.kwargs.get('roll')
        return get_object_or_404(UserProfile, roll=roll.upper(), email_confirmed=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id != self.get_object().user.id:
            raise PermissionDenied
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)


class SocialLinkCreateView(LoginRequiredMixin, CreateView):
    model = SocialLink
    template_name = 'oauth/sociallink_create.html'
    form_class = SocialLinkForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SocialLinkCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(SocialLinkCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SocialLinkUpdateView(SocialLinkOwnerMixin, UpdateView):
    model = SocialLink
    template_name = 'oauth/sociallink_update.html'
    form_class = SocialLinkForm

    def get_object(self, queryset=None):
        user = self.kwargs.get('username')
        social_media = self.kwargs.get('social_media')  # gets social_media value from url
        return get_object_or_404(SocialLink, user__username=user, social_media=social_media)


class SocialLinkDeleteView(SocialLinkOwnerMixin, DeleteView):
    model = SocialLink

    def get_success_url(self):
        return self.request.user.userprofile.get_absolute_url()

    def get_object(self, queryset=None):
        user = self.kwargs.get('username')
        social_media = self.kwargs.get('social_media')  # gets social_media value from url
        return get_object_or_404(SocialLink, user__username=user, social_media=social_media)


class RegisterView(LoginRequiredMixin, CreateView):
    template_name = 'oauth/register.html'
    success_url = reverse_lazy('forum:index')
    form_class = UserProfileForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        response_redirect = super(RegisterView, self).form_valid(form)
        return response_redirect

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self.request.user, 'userprofile'):
            return HttpResponseRedirect(reverse('oauth:detail', kwargs={'roll': self.request.user.userprofile.roll}))
        else:
            return super().dispatch(request, args, kwargs)


class AccountActivationView(RedirectView):
    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        activated_user = UserProfile.objects.activate_account(uidb64=uidb64, token=token)

        if activated_user:
            return redirect(activated_user.userprofile.get_absolute_url())
        else:
            # invalid link
            return render(self.request, 'oauth/invalid_activation.html')


def get_activation_link(request, roll):
    userprofile = UserProfile.objects.get(roll=roll.upper())
    return render(request, 'oauth/account_activation_email.html', {'user': userprofile.user})


class SessionView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        key = self.request.user.social_auth.get(provider="google-oauth2").extra_data['access_token']
        response = HttpResponseRedirect("/login?key=" + key)
        return response
