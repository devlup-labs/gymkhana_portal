from django.contrib import admin
from .models import Society, Club, SocialLink, Senate, SenateMembership, Festival, Activity, Contact, Faculty,FacultySocialLink

class MembershipInline(admin.StackedInline):
    model = SenateMembership
    can_delete = True
    verbose_name_plural = 'Members'


class SenateAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class SocietyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", "year")}
    list_display = ('name', 'is_active', 'year')
    list_filter = ('year', 'is_active')

class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    can_delete = True
    verbose_name_plural = 'Social Links'

class ClubAdmin(admin.ModelAdmin):
    inlines = (SocialLinkInline,)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'society__name']
    list_display = ('__str__', 'society', 'ctype', 'published')
    list_filter = ('published', 'ctype')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'club')


class FacultySocialLinkInline(admin.StackedInline):
    model = FacultySocialLink
    can_delete = True
    verbose_name_plural = 'Social Links'


class FacultyAdmin(admin.ModelAdmin):
    inlines = (FacultySocialLinkInline,)
    list_display = ( 'first_name','last_name','staff_status',)
    list_filter = ('staff_status','gender','department',)

# iterable list
main_models = [
    Festival,
    Contact
]

admin.site.register(Society, SocietyAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Senate, SenateAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(main_models)
admin.site.register(Faculty,FacultyAdmin)
