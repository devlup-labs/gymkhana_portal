from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, RedirectView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from .mixins import SocialLinkOwnerMixin
from .models import UserProfile, SocialLink
from .forms import UserProfileUpdateForm, SocialLinkForm, SignUpForm
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
        if request.user.is_authenticated() and request.user.id is not self.get_object().user.id:
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


class RegisterView(CreateView):
    model = UserProfile
    template_name = 'oauth/register.html'
    success_url = reverse_lazy('oauth:register-success')
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        RegisterView.create_profile(user, **form.cleaned_data)
        messages.success(self.request, user.get_full_name(), extra_tags='username')
        messages.success(self.request, user.userprofile.get_activation_url, extra_tags='activation-link')
        return super(RegisterView, self).form_valid(form)

    @staticmethod
    def create_profile(user=None, **kwargs):
        # Creates a new UserProfile object after successful creation of User object
        userprofile = UserProfile.objects.create(user=user, gender=kwargs['gender'], roll=kwargs['roll'],
                                                 dob=kwargs['dob'], prog=kwargs['prog'], year=kwargs['year'],
                                                 phone=kwargs['phone'], branch=kwargs['branch'])
        userprofile.save()

        # def dispatch(self, request, *args, **kwargs):
        #     if self.request.user.is_authenticated:
        #         logout(self.request)
        #     return super(RegisterView, self).dispatch(request, *args, *kwargs)


class RegisterSuccessView(TemplateView):
    template_name = 'oauth/register_success.html'


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
