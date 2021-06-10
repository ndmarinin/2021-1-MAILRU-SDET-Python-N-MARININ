import allure
import pytest
from api.client.api_client import ApiClient
from database.builder.mysql_orm_builder import MySqlOrmBuilder
from database.client.mysql_orm_client import SQLOrmClient
from functions.rand_user import create_user


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

    @pytest.mark.API_DB
    @allure.title("Проверка добавление валидного пользователя в базе")
    @allure.description("""
            Тестируется добавление валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на добавление валидного пользователя.
            Ожидается появления записи в базе данных.
        """)
    def test_add_user(self):
        username, email, password = create_user()
        self.api_client.add_user(username, password, email)
        assert self.MySqlBuilder.get_user(username) is not None

    @pytest.mark.API_DB
    @allure.title("Проверка добавление существующего валидного пользователя в базе")
    @allure.description("""
            Тестируется добавление существующего валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на добавление валидного пользователя.
            Ожидается существования записи в базе данных.
        """)
    def test_add_exist_user(self, user):
        username, email, password = user
        self.api_client.add_user(username, password, email)
        assert self.MySqlBuilder.get_user(username) is not None


    @pytest.mark.API_DB
    @allure.title("Проверка удаления существующего валидного пользователя в базе")
    @allure.description("""
            Тестируется удаления существующего валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на удаления валидного пользователя.
            Ожидается удаления записи в базе данных.
        """)
    def test_del_exist_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.delete_user(username)
        assert self.MySqlBuilder.get_user(username) is None

    @pytest.mark.API_DB
    @allure.title("Проверка добавления несуществующего пользователя в базе")
    @allure.description("""
            Тестируется удаления несуществующего пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на удаления несуществующего пользователя.
            Ожидается неизменость базы данных.
        """)
    def test_del_nonexistent_user(self):
        username = 'dasdjq'
        self.api_client.delete_user(username)
        assert self.MySqlBuilder.get_user(username) is None

    @pytest.mark.API_DB
    @allure.title("Проверка блокировка валидного пользователя в базе")
    @allure.description("""
            Тестируется блокировка валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на блокировку существующего пользователя.
            Ожидается что поле доступа изменится на 0 в базе данных.
        """)
    def test_block_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.block_user(username)
        assert self.MySqlBuilder.get_user(username).access == 0

    @pytest.mark.API_DB
    @allure.title("Проверка локировка заблокированного пользователя в базе")
    @allure.description("""
            Тестируется блокировка заблокированного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на блокировку заблокированного существующего пользователя.
            Ожидается что поле доступа неизменится в базе данных.
        """)
    def test_negative_block_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        self.api_client.block_user(username)
        assert self.MySqlBuilder.get_user(username).access == 0

    @pytest.mark.API_DB
    @allure.title("Проверка разблокировка валидного пользователя в базе")
    @allure.description("""
            Тестируется разблокировка валидного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Запрос на разблокировку существующего пользователя.
            Ожидается что поле доступа изменится на 1 в базе данных.
        """)
    def test_unblock_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 0, 0)
        self.api_client.unblock_user(username)
        assert self.MySqlBuilder.get_user(username).access == 1

    @pytest.mark.API_DB
    @allure.title("Проверка данных в базе разблокировка незаблокированного пользователя")
    @allure.description("""
            Тестируется разблокировка незаблокированного пользователя через api и проверка записи в базе данных.
            Шаги:
            1. Добавление юзера
            2. Ззапрос на разблокировку не заблокированного существующего пользователя.
            Ожидается что поле доступа неизменится в базе данных.
        """)
    def test_negative_unblock_user(self):
        username, email, password = create_user()
        self.MySqlBuilder.add_user(username, email, password, 1, 0)
        self.api_client.unblock_user(username)
        assert self.MySqlBuilder.get_user(username).access == 1

    @pytest.mark.API_DB
    @allure.title("Проверка данных в базе пользователя после деавторизации")
    @allure.description("""Проверка данных пользователя после деавторизации.
        Шаги:
        1. Добавление юзера
        2. Деавторизация пользователя.
        3. Статус active должен стать 0.
        """)
    def test_logout_data(self):
        username, email, password = create_user()
        self.api_client.add_user(username, password, email)
        self.api_client.auth(username, password)
        self.MySqlBuilder.get_user(username)
        self.api_client.logout()
        assert self.MySqlBuilder.get_user(username).access == 0

    @pytest.mark.API_DB
    @allure.title("Проверка блокировки пользователя при активной сессии")
    @allure.description("""Проверка блокировки пользователя при активной сессии
        Шаги:
        1. Добавлене пользователя
        2. Авторизация
        3. Блокировка
        4. Получение статуса пользователя
        5. Получение активности пользователя
        """)
    def test_block_active_session(self):
        username, email, password = create_user()
        self.api_client.add_user(username, password, email)
        self.api_client.auth(username, password)
        self.api_client.block_user(username)
        assert self.MySqlBuilder.get_user(username).access == 1
        assert self.MySqlBuilder.get_user(username).active == 0
