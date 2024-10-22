from rest_framework.test import APITransactionTestCase
import json
from django.core.exceptions import ObjectDoesNotExist

from .models import Pereval, CustomUser


class PerevalTestCase(APITransactionTestCase):
    # Это понижает скорость тестов, но позволяет делать ресет для ID в каждом тесте
    reset_sequences = True

    def setUp(self):
        self.url = '/perevals/'
        with open('request.json', 'r', encoding="utf8") as file:
            self.data = json.load(file)

    # Тест для поста
    def test_post(self):
        # Пытаемся создать объект
        response = self.client.post(self.url, self.data)
        # Проверяем что сообщение верно
        self.assertEqual(response.content.decode('utf8'), '{"message":"Отправлено успешно","id":1}')
        # Получаем созданный перевал
        response = self.client.get(self.url + '1/')
        created = json.loads(response.content)
        # Удаляем поля, которые не передаются
        del created['id']
        del created['add_time']
        del created['status']
        # Проверяем что объект равен тому что мы передали
        self.assertEqual(created, self.data)

        # Проверяем отсутствие дублирования юзеров
        self.client.post(self.url, self.data)
        # Проверяем существование юзера, если его нету то вызовет ошибку
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(id=2)

        # Проверим что юзер не создастся если менять не почту
        test_data = self.data
        test_data['user']['otc'] = 'Ivanovich'
        self.client.post(self.url, test_data)
        # Опять проверяем существование юзера
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(id=2)

        # Проверим что создание второго юзера возможно при изменении почты
        test_data['user']['email'] = 'testdata@mail.ru'
        self.client.post(self.url, test_data)
        # Получим второго юзера и проверим что его данные отличаются
        second = CustomUser.objects.get(id=2)
        self.assertEqual(second.email, 'testdata@mail.ru')
        self.assertEqual(second.otc, 'Ivanovich')

    # Тесты для патча
    def test_patch(self):
        # Создаем объект, который будем менять
        self.client.post(self.url, self.data)
        # Меняем объект
        self.client.patch(self.url + '1/', {"beauty_title": "per."})
        # Получаем измененный объект
        response = self.client.get(self.url + '1/')
        changed = json.loads(response.content)
        # Проверяем что значение изменено
        self.assertEqual(changed['beauty_title'], 'per.')

        # Пытаемся поменять юзера
        response = self.client.patch(self.url + '1/', {"user": {"otc": "Ivanovich", }})
        # Проверяем что выдает ошибку
        self.assertEqual(response.content.decode('utf8'),
                         '{"state":0,"message":"данные пользователя нельзя переопределить"}'
                         )
        # Проверим что сам объект не изменен
        response = self.client.get(self.url + '1/')
        changed = json.loads(response.content)
        self.assertNotEqual(changed['user']['otc'], 'Ivanovich')

        # Пытаемся поменять не новый объект
        # Получаем объект и меняем его статус, это нельзя сделать через запросы
        thing = Pereval.objects.get(id=1)
        thing.status = 'AC'
        thing.save()
        # Пытаемся поменять объект
        response = self.client.patch(self.url + '1/', {"beauty_title": "far."})
        # Проверяем что получили ошибку
        self.assertEqual(response.content.decode('utf8'),
                         '{"state":0,"message":"Этот объект не является новым и поэтому не может быть изменен"}')
        # Проверим что сам объект не изменен
        response = self.client.get(self.url + '1/')
        changed = json.loads(response.content)
        self.assertNotEqual(changed['beauty_title'], 'far.')

    # Лист не проверяется, ибо он не изменен.
    # Фильтрование не проверяется, поскольку сделано все встроенными методами.
