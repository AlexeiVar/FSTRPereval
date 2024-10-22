from rest_framework.test import APITransactionTestCase
import json

from .models import Pereval


class PerevalTestCase(APITransactionTestCase):
    # Это понижает скорость тестов, но позволяет делать ресет для АЙДИ в каждом тесте
    reset_sequences = True

    def setUp(self):
        self.url = '/perevals/'
        with open('request.json', 'r', encoding="utf8") as file:
            self.data = json.load(file)

    # Тест для создания
    def test_create(self):
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
