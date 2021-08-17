from selenium.webdriver import ActionChains
import allure
from functions.rand_user import create_user
from ui.fixtures.pageObject_fixtures import *
from ui.tests.base import BaseCase
from api.client.vk_api_client import VkApiClient


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

    @pytest.mark.UI
    @allure.title("Авторизация пользователя через UI")
    @allure.description("""
            Тестируется авторизация пользователя через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Авторизация через форму.
            Ожидается имя пользователя на главной странице.
        """)
    def test_auth(self, user):
        username, password, email = user
        self.base_page.auth(username, password)
        assert username in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Авторизация заблокированного пользователя через UI")
    @allure.description("""
            Тестируется авторизация заблокированного пользователя через UI .
            Шаги:
            1. Создается заблокированный пользователь через базу данных.
            2. Авторизация через форму.
            Ожидается что авторизация не пройдет.
        """)
    def test_auth_via_blocked_user(self, blocked_user):
        username, password, email = blocked_user
        self.base_page.auth(username, password)
        assert 'Ваша учетная запись заблокирована' in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Авторизация несуществующего пользователя через UI")
    @allure.description("""
            Тестируется авторизация несуществующего пользователя через UI .
            Шаги:
            1. Авторизация через форму.
            Ожидается что авторизация не пройдет.
        """)
    def test_negative_auth(self):
        username, password, email = create_user()
        self.base_page.auth(username, password)
        assert 'Invalid username or password' in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Регистрация пользователя через UI")
    @allure.description("""
            Тестируется регистрация пользователя через UI .
            Шаги:
            1. Регистрация в приложении.
            Ожидается что регистрация пройдет.
        """)
    def test_reg(self):
        self.base_page.go_to_reg()
        username, email, password = create_user()
        home = self.reg_page.register_user(username=username, email=email, password=password)
        assert_str = home.get_login_name()
        assert assert_str in self.driver.page_source
        self.MySqlBuilder.del_user(username)

    @pytest.mark.UI
    @allure.title("Регистрация существуещего пользователя через UI")
    @allure.description("""
            Тестируется регистрация существуещего пользователя через UI .
            Шаги:
            1. Регистрация в приложении.
            2. Выход из аккаунта.
            3. Происходит регистрация через форму.
            Ожидается что регистрация не пройдет.
        """)
    def test_negative_reg(self):
        self.base_page.go_to_reg()
        username, email, password = create_user()
        home_pg = self.reg_page.register_user(username=username, email=email, password=password)
        home_pg.click(self.home_page.locators.LOGOUT_BUTTON_LOCATOR, 10)
        self.base_page.go_to_reg()
        self.reg_page.register_user(username, email, password)
        assert 'User already exist' in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест регистрации с дублем по почте")
    @allure.description("""
            Тестируется регистрация пользователя через UI c дублем по еmail.
            Шаги:
            1. Регистрация в приложении.
            2. Выход
            3. Регистрация с новыми данными, но дублем по email
            В ответе ожидается сообщение об ошибке.
        """)
    def test_register_dublicate_email(self):
        self.base_page.go_to_reg()
        username1, email1, password1 = create_user()
        username2, email2, password2 = create_user()
        home_pg = self.reg_page.register_user(username=username1, email=email1, password=password1)
        home_pg.click(self.home_page.locators.LOGOUT_BUTTON_LOCATOR, 10)
        self.base_page.go_to_reg()
        self.reg_page.register_user(username=username2, email=email1, password=password2)
        assert "Email already exist" in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест регистрации с невалидными данными")
    @allure.description("""
            Тестируется регистрация пользователя через UI со всеми невалидными данными.
            Шаги:
            1.Регистрация в приложении.
            В ответе ожидается сообщение об ошибке email pass username.
        """)
    def test_all_not_valid(self):
        username, email, password = create_user(valid_email=False, valid_password=False, valid_username=False)
        self.base_page.go_to_reg()
        self.reg_page.register_user(username=username, email=email, password=password)
        assert "Email already exist" in self.driver.page_source
        assert 'User already exist' in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест регистрации с неправильным повтором пароля")
    @allure.description("""
            Тестируется регистрация пользователя через UI со неправильным повтором пароля.
            Шаги:
            1.Регистрация в приложении.
            В ответе ожидается сообщение об ошибке нессответствия паролей.
        """)
    def test_invalid_password_match(self):
        username, email, password = create_user()
        self.base_page.go_to_reg()
        self.reg_page.register_user(username=username, email=email, password=password, mismatch=True)
        assert self.reg_page.find(self.reg_page.locators.PASSWORD_MISMATCH, timeout=2).is_displayed()

    @pytest.mark.UI
    @pytest.mark.parametrize('LOCATORS', [
        ['SMTP_HREF_LOCATOR', 'SMTP'],
        ['INTERNET_HREF_LOCATOR', 'What Will the Internet Be Like in the Next 50 Years?'],
        ['API_HREF_LOCATOR', 'API'],

    ])
    @allure.title("Тест ссылок на главной странице")
    @allure.description("""
            Тестируется ссылка на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт
        """)
    def test_main_urls(self, user, LOCATORS):
        locator = getattr(self.home_page.locators, LOCATORS[0])
        assert_string = LOCATORS[1]
        username, password, _ = user
        self.base_page.auth(username, password)
        self.home_page.click(locator)
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert assert_string in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест главного меню")
    @allure.description("""
            Тестируются кнопки меню на главной страницу через UI .
            Шаги:
            1. Создается пользователь через базу данных.
            2. Переходим по ссылке.
            Ожидается что ссылка введет на сайт с локатором <LOCATORS>.
        """)
    @pytest.mark.parametrize('LOCATORS', [
        ['HOME_MENU_LOCATOR', 'powered by ТЕХНОАТОМ', 'HOME_MENU_LOCATOR'],
        ['PYTHON_MENU_LOCATOR', 'Python is a programming language that lets you work quickly', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_HISTORY_MENU_LOCATOR', 'History of Python', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_FLASK_MENU_LOCATOR', 'User’s Guide', 'PYTHON_MENU_LOCATOR'],
        ['CENTOS_BUTTON_LOCATOR', 'centos', 'LINUX_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_NEWS_MENU_LOCATOR', 'Wireshark 3.4.6 and 3.2.14 Released', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_DOWNLOAD_MENU_LOCATOR', 'Download Wireshark', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_TCPDUMP_MENU_LOCATOR', 'Tcpdump Examples', 'NETWORK_MENU_LOCATOR'],
    ])
    def test_menu(self, LOCATORS, user):

        username, password, _ = user
        self.base_page.auth(username, password)
        locator = getattr(self.home_page.locators, LOCATORS[0])
        hover_element = self.base_page.find(getattr(self.home_page.locators, LOCATORS[2]))
        hover = ActionChains(self.driver).move_to_element(hover_element)
        hover.perform()
        self.home_page.click(locator)
        if len(self.driver.window_handles) == 2:
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
        assert LOCATORS[1] in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест видимости меню при масштабировании")
    @allure.description(""" Корректность меню при уменьшении страницы.
        Уменьшение окна и поиск кнопки home.
        Кнопка Home видима и доступна.
        """)
    def test_window_size(self, user):
        username, password, _ = user
        self.base_page.auth(username, password)

        self.driver.set_window_size(350, 750)

        assert self.home_page.find(self.home_page.locators.HOME_MENU_LOCATOR, 1).is_displayed()
        self.driver.maximize_window()

    @pytest.mark.UI
    @allure.title("Тест получения данных с мока")
    @allure.description("""Тестируются получения данных с мока и отображение на UI .
        Шаги:
        1. Создается пользователь
        2. Добавляется в мок
        3. Првоеряется соответсвие данных с мока и в UI""")
    def test_vk(self, user):
        username, password, _ = user
        self.host = "vk_api"
        self.post = 5000
        self.VK_API = VkApiClient()
        id = self.VK_API.post_add_user(username=username)
        self.base_page.auth(username, password)
        vk_id = self.home_page.find(self.home_page.locators.LOG_VK_ID, timeout=3).text
        name = self.home_page.find(self.home_page.locators.LOG_USERNAME, timeout=3).text
        vk_id = int(vk_id.split()[-1])
        name = name.split()[-1]
        assert vk_id == id
        assert name == username

    @pytest.mark.UI
    @allure.title("Тест сообщения о несуществующей страницы")
    @allure.description("Тестируются открытие несуществующей страницы Шаги:1. Открывается рандомный урл")
    def test_404_error(self):
        self.base_page.go_to_random_url()
        assert "Page Not Found" in self.driver.page_source

    @pytest.mark.UI
    @allure.title("Тест откртия ссылок в новых вкладках")
    @pytest.mark.parametrize('LOCATORS', [
        ['PYTHON_MENU_LOCATOR', 'Welcome to ', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_HISTORY_MENU_LOCATOR', 'History of Python', 'PYTHON_MENU_LOCATOR'],
        ['PYTHON_FLASK_MENU_LOCATOR', 'Welcome to Flask', 'PYTHON_MENU_LOCATOR'],
        ['CENTOS_BUTTON_LOCATOR', 'Download', 'LINUX_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_NEWS_MENU_LOCATOR', 'Wireshark', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_WIRESHARK_DOWNLOAD_MENU_LOCATOR', 'Wireshark', 'NETWORK_MENU_LOCATOR'],
        ['NETWORK_TCPDUMP_MENU_LOCATOR', 'Tcpdump Examples', 'NETWORK_MENU_LOCATOR'],
    ])
    def test_tabs(self, user, LOCATORS):
        username, password, _ = user
        self.base_page.auth(username, password)
        locator = getattr(self.home_page.locators, LOCATORS[0])
        locator2 = getattr(self.home_page.locators, LOCATORS[2])
        origin_tile = LOCATORS[1]
        events = self.base_page.find(locator2, timeout=3)
        ac = ActionChains(self.driver)
        ac.move_to_element(events).perform()
        self.base_page.find(locator).click()
        windows = self.driver.window_handles
        assert len(windows) == 2
        self.driver.switch_to.window(windows[1])
        title = self.driver.title
        assert origin_tile in title

