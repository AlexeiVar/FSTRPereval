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
            data = request.data
            if 'user' in data:
                # Если юзер Null, то пропускаю все
                if data['user'] is None:
                    pass
                else:
                    # Если передали юзера то проверяю что он не изменен
                    user_dict = model_to_dict(instance.user)
                    # В дате нету айди юзера, поэтому удаляю его из нашего словаря
                    del user_dict['id']
                    if not data['user'] == user_dict:
                        response = {'state': 0, 'message': 'данные пользователя нельзя переопределить'}
                        return Response(response)

            coords_instance = instance.coords
            images_instance = Images.objects.filter(pereval=instance.id)
            # Если нам прислали изображения, то работаем с ними
            if 'images' in data:
                # Удаляем все изображения, ибо это легче чем изменять их
                # это лучше решение только пока в images.data хранится ссылка или путь к файлу, а не сам файл
                for image in images_instance:
                    image.delete()
                for image_data in data['images']:
                    image = Images(data=image_data['data'], title=image_data['title'], pereval=instance)
                    image.save()
            # переопределяю поля перевала если они меняются, сохранение все равно произойдет
            if 'beauty_title' in data:
                instance.beauty_title = data['beauty_title']
            if 'title' in data:
                instance.title = data['title']
            if 'other_titles' in data:
                instance.other_titles = data['other_titles']
            if 'connect' in data:
                instance.connect = data['connect']
            instance.save()
            # Смотрю есть ли сложность в присланных данных
            if 'level' in data:
                level_instance = instance.level
                level_data = data['level']
                # переопределяю поля сложности в цикле
                for season in level_data:
                    # Прохожусь по каждому переданному сезону и заменяю уровень сложности
                    level_instance.__setattr__(season, level_data[season])
                level_instance.save()

            # переопределяю поля координат
            coords_instance.latitude = data['coords']['latitude']
            coords_instance.longitude = data['coords']['longitude']
            coords_instance.height = data['coords']['height']

            coords_instance.save()
            response = {'state': 1}
            return Response(response)
        else:
            response = {'state': 0, 'message': 'Этот объект не является новым и поэтому не может быть изменен'}
            return Response(response)

    # Делаю возможность поиска по почте через queryset
    def get_queryset(self):
        queryset = self.queryset
        # Пытаюсь получить почту из ссылки
        email = self.request.query_params.get('user__email')
        # Для лучшей читабельности делаю is not None а не просто if
        if email is not None:
            # Если почта есть, то меняю фильтр
            queryset = queryset.filter(user__email=email)
        # Возвращаю фильтр
        return queryset
