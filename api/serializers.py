from collections import OrderedDict

from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework import serializers

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


class ProfileSerializer(DiyBlogModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'
