from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('name', 'club', 'date', 'location')
    list_filter = ('date',)

    class Meta:
        model = Event


admin.site.register(Event, EventAdmin)
