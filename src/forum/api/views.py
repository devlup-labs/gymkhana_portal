from rest_framework.views import APIView
from rest_framework.response import Response
from forum.models import Topic, Answer
from django.shortcuts import get_object_or_404


class TopicUpvoteAPIToggle(APIView):
    def get(self, request, slug=None, format='json'):
        obj = get_object_or_404(Topic, slug=slug)
        user = self.request.user
        updated = False
        upvoted = False
        if user.is_authenticated:
            if user.userprofile in obj.upvotes.all():
                obj.upvotes.remove(user.userprofile)
                upvoted = False
            else:
                obj.upvotes.add(user.userprofile)
                upvoted = True
            updated = True
        data = {
            'updated': updated,
            'upvoted': upvoted
        }
        return Response(data)


class AnswerUpvoteAPIToggle(APIView):
    def get(self, request, id=None, format=None):
        obj = get_object_or_404(Answer, id=id)
        user = self.request.user
        updated = False
        upvoted = False
        if user.is_authenticated:
            if user.userprofile in obj.upvotes.all():
                obj.upvotes.remove(user.userprofile)
                upvoted = False
            else:
                obj.upvotes.add(user.userprofile)
                upvoted = True
            updated = True
        data = {
            'updated': updated,
            'upvoted': upvoted
        }
        return Response(data)
