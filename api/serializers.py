from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from Blog import models


class IDPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        return data


class DiyBlogModelSerializer(serializers.ModelSerializer):
    def get_fields(self):
        """By default, choice fields are serialized only with the choice value, not the human readable
        text.
        For convenience we add an additional field "[field name]_display" with the human readable
        display value.
        """
        fields = OrderedDict()
        for key, value in super().get_fields().items():
            fields[key] = value
            if isinstance(value, serializers.ChoiceField):
                fields[key + "_display"] = serializers.CharField(source="get_{}_display".format(key), read_only=True)

            # Every IDPrimaryKeyRelatedField is suffixed with `_id` to match the foreign key field
            if isinstance(value, IDPrimaryKeyRelatedField):
                fields[f"{key}_id"] = value
                del fields[key]
        return fields


class DiyContentModelSerializer(DiyBlogModelSerializer):
    content = serializers.ModelField(model_field=models.ContentModelMixin()._meta.get_field('content'))
    created = serializers.DateField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)


class ProfileSerializer(DiyBlogModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'


class PostSerializer(TaggitSerializer, DiyContentModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = models.Post
        fields = ('title', 'content', 'created', 'vote_score', 'tags', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_joined', 'last_login', 'groups')


class CommentSerializer(DiyContentModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('content', 'created', 'user', 'post')
