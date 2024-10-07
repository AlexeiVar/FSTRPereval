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
        ]
        read_only_fields = ['status',]
