import pytest
import time

import basic_locators

login = "vosaco7441@leonvero.com"
password = "vosaco7441"
CLICK_RETRY = 3


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config




    def find(self, locator):
        return self.driver.find_element(*locator)

    def get_field(self, locator):
        element = self.driver.find_element(*locator)
        return element.get_attribute("value")

    def click(self, locator):
        element = self.find(locator)
        element.click()

    def enter_data(self, locator, data):
        element = self.find(locator)
        element.click()
        element.clear()
        element.send_keys(data)

    def enter_creds(self, login, password):
        time.sleep(1)
        self.click(basic_locators.LOGIN_MENU)
        self.enter_data(basic_locators.EMAIL, login)
        self.enter_data(basic_locators.PASS, password)
        self.click(basic_locators.LOGIN_BUTTON)

    def enter_info(self, fio, tel, mail):
        self.enter_data(basic_locators.FIO_FIELD, fio)
        self.enter_data(basic_locators.PHONE_FIELD, tel)
        self.enter_data(basic_locators.MAIL_FIELD, mail)
        self.click(basic_locators.SAVE_BUTTON)







