from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin

from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring'
        ]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'phone',
            'email',
            'fam',
            'name',
            'otc'
        ]


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'data',
            'title',
            'pereval',
        ]
        read_only_fields = ['pereval',]


class PerevalSerializer(WritableNestedModelSerializer):
    images = ImagesSerializer(many=True)
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer()
    class Meta:
        model = Pereval
        fields = [
            'add_time',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'status',
            'level',
            'coords',
            'images',
            'user',
        ]
        read_only_fields = ['status',]

    def create(self, validated_data, **kwargs):
        level = validated_data.pop('level')
        coords = validated_data.pop('coords')
        images = validated_data.pop('images')
        user = validated_data.pop('user')
        user, created = CustomUser.objects.get_or_create(**user)

        level = Level.objects.create(**level)
        coords = Coords.objects.create(**coords)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(data=data, pereval=pereval, title=title)

        return pereval

