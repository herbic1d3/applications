from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from blueprints.models import Blueprint
from keys.models import Key


class BlueprintTestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    class Meta:
        model = Blueprint
        fields = ('id', 'title', 'created')


class BlueprintSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    key = serializers.PrimaryKeyRelatedField(queryset=Key.objects.all())
    title = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = Blueprint
        fields = ('id', 'title', 'key')

    def validate(self, attrs):
        if not len(attrs['title']):
            raise ValidationError("Title can't be empty")
        return attrs
