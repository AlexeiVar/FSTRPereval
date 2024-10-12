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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        user_dict = model_to_dict(instance.user)
        # В дате нету айди юзера, поэтому удаляю его из нашего словаря
        del user_dict['id']
        if not data['user'] == user_dict:
            response = {'state': 0, 'message': 'данные пользователя нельзя переопределить'}
            return Response(response)
        response = {'state': 1}
        return Response(response)
