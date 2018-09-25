import datetime

from rest_framework import viewsets, permissions

from api import serializers, utils
from Blog import models


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        slug = utils.get_slug(self.request.data.get('title'), models.Post)
        created = datetime.date.today()
        serializer.save(user=self.request.user, slug=slug, created=created)

