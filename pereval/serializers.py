from drf_writable_nested import UniqueFieldsMixin, NestedUpdateMixin

from .models import *
from rest_framework import serializers, status
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.response import Response


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
        read_only_fields = ['pereval', ]


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
        read_only_fields = ['status', 'add_time']

    def create(self, validated_data, **kwargs):
        level = validated_data.pop('level')
        coords = validated_data.pop('coords')
        images = validated_data.pop('images')
        user = validated_data.pop('user')
        # Этот get_or_create проверяет только почту, если такая есть то он не создаст юзера
        # иначе он создаст юзера, помещая туда все данные из defaults
        user, created = CustomUser.objects.get_or_create(email=user['email'], defaults={
            'fam': user['fam'], 'name': user['name'], 'otc': user['otc'], 'phone': user['phone']
        })

        level = Level.objects.create(**level)
        coords = Coords.objects.create(**coords)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level)

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Images.objects.create(data=data, pereval=pereval, title=title)

        return pereval
