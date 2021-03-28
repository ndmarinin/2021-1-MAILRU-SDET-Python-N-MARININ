import pytest
import time
from base import BaseCase
import basic_locators

email = "567@mail.ru"
phone = "123"
name = "ABC"

login = "vosaco7441@leonvero.com"
password = "vosaco7441"


class TestOne(BaseCase):
    @pytest.fixture()
    def driver_auth(self, driver, config):
        self.driver = driver
        self.config = config
        self.enter_creds(login, password)

    def test_do_login(self):
        time.sleep(2)
        self.enter_creds(login, password)
        time.sleep(2)
        assert "Кампании" in self.driver.title

    def test_edit_info(self, driver_auth):
        time.sleep(3)
        self.click(basic_locators.EDIT_PROFILE)
        time.sleep(2)
        self.enter_info(name, phone, email)
        time.sleep(2)
        source = self.driver.page_source
        print(self.get_field(basic_locators.FIO_FIELD))
        assert name in self.get_field(basic_locators.FIO_FIELD)
        assert phone in self.get_field(basic_locators.PHONE_FIELD)
        assert email in self.get_field(basic_locators.MAIL_FIELD)

    @pytest.mark.parametrize('section', ['BILLING', 'STATS'])
    def test_category(self, section, driver_auth):
        time.sleep(2)
        self.enter_category(section)

    def test_logout(self, driver_auth):
        time.sleep(2)
        self.click(basic_locators.PROFILE)
        time.sleep(1)
        self.click(basic_locators.LOGOUT)
        time.sleep(1)
        assert "Войти" in self.driver.page_source

