from django.contrib import admin
from .models import Topic, Answer


class TopicAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)

    class Meta:
        model = Topic


admin.site.register(Topic, TopicAdmin)


class AnswerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('topic', 'author', 'created_at')
    list_filter = ('created_at',)

    class Meta:
        model = Answer


admin.site.register(Answer, AnswerAdmin)
