from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from oauth.models import UserProfile, SocialLink


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    can_delete = True
    verbose_name_plural = 'Social Links'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, SocialLinkInline)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'link')


admin.site.register(SocialLink, SocialLinkAdmin)
