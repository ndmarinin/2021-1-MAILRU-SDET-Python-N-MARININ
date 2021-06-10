import allure

from functions.rand_user import create_user
from ui.tests.base import BaseCase
from ui.fixtures.pageObject_fixtures import *

class TestUI(BaseCase):

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

    @pytest.mark.UI_DB
    @allure.title("Тест регистрация пользователя через UI и првоерка в базе")
    @allure.description("""
            Тестируется регистрация пользователя через UI и проверка записи в базе данных.
            Шаги:
            1. Регистрация через форму.
            Ожидается что регистрация пройдет и в базе данных появится запись.
        """)
    def test_reg(self):
        username, email, password = create_user()
        self.base_page.go_to_reg()
        self.reg_page.register_user(username, email, password)
        assert self.MySqlBuilder.get_user(username) is not None
        self.MySqlBuilder.del_user(username)

    @pytest.mark.UI_DB
    @allure.title("Тест регистрация пользователя через UI и проверка в базе")
    @allure.description("""
            Тестируется регистрация существуещего пользователя через UI и проверка записи в базе данных.
            Шаги:
            1. Регистрация через форму.
            2. Регистрация через форму.
            Ожидается что запись будет добавлена один раз в базу данных.
        """)
    def test_negative_reg(self):
        username, email, password = create_user()
        self.base_page.go_to_reg()
        self.reg_page.register_user(username, email, password)
        self.home_page.click(self.home_page.locators.LOGOUT_BUTTON_LOCATOR)
        self.base_page.go_to_reg()
        self.reg_page.register_user(username, email, password)
        assert self.MySqlBuilder.get_user(username) is not None