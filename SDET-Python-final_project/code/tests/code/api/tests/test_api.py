import json

import allure
import pytest
from functions.rand_user import create_user
from api.client.api_client import ApiClient
from database.builder.mysql_orm_builder import MySqlOrmBuilder
from database.client.mysql_orm_client import SQLOrmClient

class TestApi:

    @pytest.fixture(scope='function', autouse=True)
    def client(self):
        self.api_client = ApiClient(host='myapp', port=8080)
        self.MySqlClient = SQLOrmClient(user='test_qa', password="qa_test", host='mysql', port=3306, db_name='test')
        self.MySqlBuilder = MySqlOrmBuilder(self.MySqlClient)
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username=username, email=email, password=password, access=1, active=0)
        self.api_client.auth(username, password)
        yield self.api_client
        self.MySqlBuilder.del_user(username)
        self.MySqlClient.close_connect()

    @pytest.fixture(scope='function')
    def user(self):
        username, email, password = create_user()
        user = self.MySqlBuilder.add_user(username=username, email=email, password=password, access=1, active=0)
        yield username, password, email
        self.MySqlBuilder.del_user(username)

    @pytest.fixture(scope='function')
    def blocked_user(self):
        username, email, password = create_user()
        user = self.MySqlBuilder.add_user(username=username, email=email, password=password, access=0, active=0)
        yield username, password, email
        self.MySqlBuilder.del_user(username)

    @pytest.mark.API
    @allure.title("Проверка добавление валидного пользователя")
    @allure.description("""
            Тестируется добавление валидного пользователя через api.
            Шаги:
            1. Добавление пользователя.
            В ответе ожидается сообщение и статус-код 201.
        """)
    def test_add_user(self):
        username, email, password = create_user()
        assert self.api_client.add_user(username, password, email).status_code == 201

    @pytest.mark.API
    @allure.title("Проверка добавление пользователя c невалидным email")
    @allure.description("""
            Тестируется добавление пользователя через api c невалидным email.
            Шаги:
            1. Добавление пользователя.
            В ответе ожидается сообщение и статус-код 400.
        """)
    def test_add_user_non_valid_email(self):
        username, email, password = create_user(valid_email=False)
        assert self.api_client.add_user(username, password, email).status_code == 400

    @pytest.mark.API
    @allure.title("Проверка добавление пользователя c невалидным паролем")
    @allure.description("""
            Тестируется добавление пользователя через api c невалидным паролем.
            Шаги:
            1. Добавление пользователя.
            В ответе ожидается сообщение и статус-код 400.
        """)
    def test_add_user_non_valid_password(self):
        username, email, password = create_user(valid_password=False)
        assert self.api_client.add_user(username, password, email).status_code == 400

    @pytest.mark.API
    @allure.title("Проверка добавление пользователя c невалидным именем")
    @allure.description("""
            Тестируется добавление пользователя через api c невалидным именем.
            Шаги:
            1. Добавление пользователя.
            В ответе ожидается сообщение и статус-код 400.
        """)
    def test_add_user_non_valid_username(self):
        username, email, password = create_user(valid_username=False)
        assert self.api_client.add_user(username, password, email).status_code == 400

    @pytest.mark.API
    @allure.description("""
            Тестируется добавление пользователя через api c дублем по еmail.
            Шаги:
            1. Добавление пользователя c email.
            2. Добавление пользователя c тем же email.
            В ответе ожидается сообщение и статус-код 400.
        """)
    @allure.title("Проверка добавление пользователя c дублем по еmail")
    def test_add_user_dublicate_email(self):
        username, email, password = create_user()
        username2, email2, password2 = create_user()
        self.api_client.add_user(username, password, email)
        assert self.api_client.add_user(username2, password2, email).status_code == 400

    @pytest.mark.API
    @allure.description("""
            Тестируется добавление пользователя через api c невалидным данными.
            Шаги:
            1. Добавление пользователя.
            В ответе ожидается сообщение и статус-код 400.
        """)
    @allure.title("Проверка добавление пользователя c невалидным данными")
    def test_add_user_non_valid_all(self):
        username, email, password = create_user(valid_username=False, valid_password=False, valid_email=False)
        assert self.api_client.add_user(username, password, email).status_code == 400

    @pytest.mark.API
    @allure.title("Проверка добавление существующего валидного пользователя")
    @allure.description("""
            Тестируется добавление существующего валидного пользователя через api.
            Шаги:
            1. Добавление пользователя
            2. Добавление пользователя еще раз
            В ответе ожидается сообщение и статус-код 304.
        """)
    def test_add_exist_user(self, user):
        username, email, password = user
        assert self.api_client.add_user(username, password, email).status_code == 304

    @pytest.mark.API
    @allure.title("Проверка удаления пользователя")
    @allure.description("""
            Тестируется удаления пользователя через api.
            Шаги:
            1. Добавление пользователя
            2. Запрос на удаления существующего валидного пользователя.
            В ответе ожидается сообщение и статус-код 204.
        """)
    def test_del_exist_user(self):
        username, email, password = create_user()
        assert self.api_client.delete_user(username).status_code == 204

    @pytest.mark.API
    @allure.title("Проверка удаления несуществующего пользователя")
    @allure.description("""
            Тестируется удаления несуществующего пользователя через api.
            Шаги:
            1. Генерация имени пользователя.
            2. Отправляется запрос на удаления несуществующего валидного пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """)
    def test_del_nonexistent_user(self):
        username, email, password = create_user()
        assert self.api_client.delete_user(username).status_code == 404

    @pytest.mark.API
    @allure.title("Проверка блокировки пользователя")
    @allure.description("""
            Тестируется блокировка пользователя через api.
            Шаги:
            1. Добавление пользователя
            2. Отправляется запрос на блокировку существуещего валидного пользователя.
            В ответе ожидается сообщение и статус-код 200.
        """)
    def test_block_user(self):
        username, email, password = create_user()
        assert self.api_client.block_user(username).status_code == 200

    @pytest.mark.API
    @allure.title("Проверка блокировка заблокированного пользователя")
    @allure.description("""
            Тестируется блокировка заблокированного пользователя через api.
            Шаги:
            1. Добавление пользователя через бд с блокировкой
            2. Запрос на блокировку существуещего заблокированного валидного пользователя.
            В ответе ожидается сообщение и статус-код 304.
        """)
    def test_negative_block_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        assert self.api_client.block_user(username).status_code == 304

    @pytest.mark.API
    @allure.title("Проверка блокировка несуществуещего пользователя")
    @allure.description("""
            Тестируется блокировка несуществуещего пользователя через api.
            Шаги:
            1. Генерация имени пользователя (случайно).
            2. Отправляется запрос на блокировку несуществуещего валидного пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """)
    def test_block_nonexistent_user(self):
        username, email, password = create_user()
        assert self.api_client.block_user(username).status_code == 404

    @pytest.mark.API
    @allure.title("Проверка разблокировки пользователя")
    @allure.description("""
            Тестируется разблокировка пользователя через api.
            Шаги:
            1. Происходит авторизация в приложении.
            2. Через базу данных добавляется заблокированный пользователь.
            3. Отправляется запрос на разблокировку валидного пользователя.
            В ответе ожидается сообщение и статус-код 200.
        """)
    def test_unblock_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        assert self.api_client.unblock_user(username).status_code == 200

    @pytest.mark.API
    @allure.title("Проверка разблокировки несуществуещего пользователя")
    @allure.description("""
            Тестируется разблокировка несуществуещего пользователя через api.
            Шаги:
            1. Генерация имени пользователя (случайно).
            2. Отправляется запрос на разблокировку несуществуещего пользователя.
            В ответе ожидается сообщение и статус-код 404.
        """)
    def test_unblock_nonexistent_user(self):
        username, email, password = create_user()
        assert self.api_client.unblock_user(username).status_code == 404

    @pytest.mark.API
    @allure.title("Проверка разблокировки незаблокированного пользователя")
    @allure.description("""
            Тестируется разблокировка незаблокированного пользователя через api.
            Шаги:
            1. Добавление пользователя через бд с блокировкой
            2. Отправляется запрос на разблокировку валидного пользователя.
            В ответе ожидается сообщение и статус-код 304.
        """)
    def test_negative_unblock_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        assert self.api_client.unblock_user(username).status_code == 304

    @allure.title("Проверка авторизация заблокированного пользователя")
    @allure.description("""
            Тестируется авторизация через заблокированного пользователя через api.
            Шаги:
            1. Добавление пользователя через бд с блокировкой
            2. Отправляется запрос на авторизацию через заблокированного пользователя.
            В ответе ожидается сообщение и статус-код 401.
        """)
    @pytest.mark.API
    def test_auth_via_blocked_user(self, blocked_user):
        username, email, password = blocked_user
        self.api_client.logout()
        assert self.api_client.auth(username, password).status_code == 401

    @allure.title("Проверка статуса приложения")
    @allure.description("""Проверка статуса приложения.
        Запрос по урлу /status.
        Ответ с сервера со статусом приложения "ok".
        """)
    @pytest.mark.API
    def test_app_ready(self):
        response = self.api_client.status()
        assert response.status_code == 200
        response = json.loads(response.text)
        assert "ok" in response["status"], response

    @allure.title("Проверка Page Not Found")
    @allure.description("""Проверка статуса несуществубщей страницы.
        Запрос по рандомному урлу.
        """)
    @pytest.mark.API
    def test_page_not_found(self):
        response = self.api_client.go_to_random_url()
        assert response.status_code == 404



