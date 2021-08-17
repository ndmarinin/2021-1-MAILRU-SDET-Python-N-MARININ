import logging
import random
import string

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.basePage_locators import BasePageLocators
LOGGER = logging.getLogger('test')
RETRY_COUNT = 10
TIMEOUT = 20


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(expected_conditions.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        LOGGER.info(f"Click on locator {locator}")
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(expected_conditions.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i > RETRY_COUNT - 1:
                    raise

    def wait(self, timeout=None):
        if timeout is None:
            timeout = TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)


    def enter_data(self, locator, data):
        LOGGER.info(f"Write {data}")
        element = self.find(locator, 5)
        self.click(locator, 5)
        element.clear()
        element.send_keys(data)

    def go_to_reg(self):
        LOGGER.info("Go to reg ")
        self.click(self.locators.CREATE_ACCOUNT_HREF_LOCATOR)

    def go_to_random_url(self):
        letters = string.ascii_lowercase
        url = self.driver.current_url
        add_str = ''.join(random.choice(letters) for i in range(5))
        url = url + add_str
        LOGGER.info(f"Go to reg {url}")
        self.driver.get(url)

    def auth(self, login, password):
        LOGGER.info(f"AUTH with login {login}, password {password}")
        self.enter_data(self.locators.LOGIN_INPUT_LOCATOR, login)
        self.enter_data(self.locators.PASSWORD_INPUT_LOCATOR, password)
        self.click(self.locators.LOGIN_BUTTON_LOCATOR)
