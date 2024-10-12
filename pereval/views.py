from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from django.forms.models import model_to_dict

from .serializers import *
from .models import *


class submitData(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Отправлено успешно', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Технически это не нужно по заданию, но поскольку наш patch это по сути put, я думаю стоит запретить настоящий put
    def update(self, request, *args, **kwargs):
        response = {'state': 0, 'message': 'используйте PATCH для изменения данных'}
        return Response(response)

    # По условию задания этот метод принимает весь json, поэтому можно было бы использовать update,
    # но по условию задания нам нужно использовать именно patch
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # проверка статуса
        if instance.status == 'NE':
            # "Метод принимает тот же самый json" является условием задания, поэтому нам не нужно проверять
            # отправлены ли данные или нет
            data = request.data
            user_dict = model_to_dict(instance.user)
            # В дате нету айди юзера, поэтому удаляю его из нашего словаря
            del user_dict['id']
            if not data['user'] == user_dict:
                response = {'state': 0, 'message': 'данные пользователя нельзя переопределить'}
                return Response(response)
            level_instance = instance.level
            coords_instance = instance.coords
            images_instance = Images.objects.filter(pereval=instance.id)
            # Удаляем все изображения, ибо это легче чем изменять их
            # это лучше решение только пока в images.data хранится ссылка или путь к файлу, а не сам файл
            for image in images_instance:
                image.delete()
            # переопределяю поля перевала
            instance.beauty_title = data['beauty_title']
            instance.title = data['title']
            instance.other_titles = data['other_titles']
            instance.connect = data['connect']
            # переопределяю поля сложности
            level_instance.winter = data['level']['winter']
            level_instance.summer = data['level']['summer']
            level_instance.autumn = data['level']['autumn']
            level_instance.spring = data['level']['spring']
            # переопределяю поля координат
            coords_instance.latitude = data['coords']['latitude']
            coords_instance.longitude = data['coords']['longitude']
            coords_instance.height = data['coords']['height']
            # создаю новые фотографии
            for image_data in data['images']:
                image = Images(data=image_data['data'], title=image_data['title'], pereval=instance)
                image.save()
            # Сохраняю изменения
            level_instance.save()
            coords_instance.save()
            instance.save()
            response = {'state': 1}
            return Response(response)
        else:
            response = {'state': 0, 'message': 'Этот объект не является новым и поэтому не может быть изменен'}
            return Response(response)
