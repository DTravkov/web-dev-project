# Все наши endpoints можно найти и посмореть по адресу (толкьо когда запустишь сервер локально) :
# http://localhost:80/api/docs ИЛИ http://127.0.0.1:80/api/docs
# Это будет твоим гланвым интерфейсом,что бы понять,как работает наш бэк и что нужно тестировать.

#Что бы запустить все тесты, используешь команду python manage.py test в консоли

# базовый класс для тестов,от него нужно наследовать что бы создать группу тестов
from rest_framework.test import APITestCase
from django.test.client import Client

# Статус коды HTTP для проверки. Посмотреть статус коды,которые мы использовали, можно в views.py
#Пример строчки : return Response(serializer.data, status=status.HTTP_200_OK)
#В этой строчке,при удачном запросе,возвращается status.HTTP_200_OK, то есть статус 200)
from rest_framework import status

#Дальше идут импорты, которые начинаются с точки. Точка в начале значит, что ты используешь файл из местной папки
#Местная папка = та,где лежит этот файл (в нашем случае это папка api)

# Здесь импортирую модели. Модели это таблицы из базы данных,нужны для создания и чтения записей в базе данных
from .models import User



# Cнизу написан класс, который проверет что пользователь может предложить дисциплину, и админ может ее подтвердить.
class PendingDisciplineAPITest(APITestCase):
    #Это функции помощники для тебя,можешь их не изучать,пользуйся для логина и логаута
    def login(self, username:str, password:str):
        response = self.client.post("/api/token/", data={"username" : username, "password" : password}, format='json')
        if response.status_code == 200:
            token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        else:
            raise Exception("Login failed")
    def logout(self):
        self.client.credentials()

    # В функции setUp необходимо создать данные и записать в базу данных.Потом созданные даныне используются в тестах.
    # В этом случае я создаю тестовых юзера и админа
    # Пример : Юзеры или Записи которые нужно отобразить
    # С помощью Model.objects.create функций можно закидывать данные в бд. Узнай как она работает,здесь не совсем понятно
    def setUp(self):

        self.USER_USERNAME = "user_test"
        self.ADMIN_USERNAME = "admin_test"

        self.TEST_PWD= "password@@@123"

        self.user = User.objects.create_user(username=self.USER_USERNAME, password=self.TEST_PWD)
        self.admin = User.objects.create_superuser(username=self.ADMIN_USERNAME,password=self.TEST_PWD)



    # Функции которые начинаются с test_ наша логика проверки. Обязательно делай приписку test_
    def test_create_pending_discipline(self):
        #Эта строчка эмулирует, что юзер залогинился. Только залогиненые юзеры могут подавать дисциплину
        self.login(username=self.USER_USERNAME, password=self.TEST_PWD)

        #Здесь я делаю HTTP POST запрос,который создает заявку на дисциплину, и записываю его ответ в response
        #Посмотреть всю инфу о запросе можно на http://localhost:80/api/docs ИЛИ http://127.0.0.1:80/api/docs
        response_create_pending = self.client.post(path="/api/pending/", data={"name" : "New Test Discipline"})

        # функции которые начинаются с self.assert, используются для проверки данных.
        # Здесь я проверяю что запрос успешный (проверяю что статус код = 200)
        self.assertEqual(response_create_pending.status_code, status.HTTP_201_CREATED)

        #Логинюсь за админа. Только он может подтверждать дисциплины
        self.logout()
        self.login(username=self.ADMIN_USERNAME, password=self.TEST_PWD)

        #Создаю и сразу проверяю другой GET запрос, который выдаст мне новую дисциплину(если она появилась)
        response_get_pending = self.client.get(path="/api/pending/" + str(response_create_pending.data['id']) + "/")
        self.assertEqual(response_get_pending.status_code, status.HTTP_200_OK)

        # Отправляю и проверяю POST который подтвердит новую дисциплину,
        response_approve_pending = self.client.post(path="/api/pending/" + str(response_create_pending.data['id']) + "/approve/")
        self.assertEqual(response_approve_pending.status_code, status.HTTP_201_CREATED)

    # Попробуй создать свой тест.
    # Он должен проверить, что незалогиненый юзер не может попросить добавить дисциплину.
    # Подсказка : Создай юзера, отправь POST запрос для добавки дисциплины ,
    # и используй self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_create_discipline_user_is_unauthorized(self):
        response = self.client.post(path="/api/pending/",data={"name": "Unauthorized Discipline"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)