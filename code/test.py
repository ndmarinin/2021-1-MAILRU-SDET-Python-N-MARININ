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

    def test_do_login(self):
        time.sleep(2)
        self.enter_creds(login, password)
        time.sleep(2)
        assert "Кампании" in self.driver.title

    def test_edit_info(self):
        time.sleep(2)
        self.enter_creds(login, password)
        time.sleep(3)
        self.click(basic_locators.EDIT_PROFILE)
        time.sleep(2)
        self.enter_info(name, phone, email)
        time.sleep(2)
        source = self.driver.page_source
        if source.__contains__(name) and source.__contains__(phone) and source.__contains__(email):
            pass



    @pytest.mark.parametrize('section', ['BILLING', 'STATS'])
    def test_category(self, section):
        time.sleep(2)
        self.enter_creds(login, password)
        time.sleep(2)
        self.enter_category(section)

    def test_logout(self):
        time.sleep(2)
        self.enter_creds(login, password)
        time.sleep(2)
        self.click(basic_locators.PROFILE)
        time.sleep(1)
        self.click(basic_locators.LOGOUT)
        assert "Войти" in self.driver.page_source
