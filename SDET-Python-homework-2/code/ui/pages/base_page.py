import logging
import os
import time
import pytest
import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators.pages_locators import BasePageLocators
from utils.decorators import wait

CLICK_RETRY = 3
BASE_TIMEOUT = 5

logger = logging.getLogger('test')


class PageNotLoadedException(Exception):
    pass





class BasePage(object):
    url = 'https://target.my.com/'
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    @allure.step('Find {locator}')
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Find {locator}')
    def find_elem(self, locator):
        logger.info(f'Find element {locator}')
        return self.driver.find_element(*locator)

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
            logger.info('Driver waiting')
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Scoll to  {element}')
    def scroll_to(self, element):
        logger.info(f'Scroll to {element}')
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    @allure.step('Enter data  {locator}')
    def enter_data(self, locator, data):
        element = self.find(locator)
        element.click()
        element.clear()
        logger.info(f'Send {data} to {locator}')
        element.send_keys(data)

    def send_data(self, locator, path ):
        element = self.find(locator)
        logger.info(f'Send file {path} to element {locator}')
        element.send_keys(path)

    def file_path(self):
        DIR = os.path.dirname(os.path.dirname(os.getcwd())) + '\data\picture.jpg'
        logger.info(f'FINDING FILE IN {DIR}')
        return DIR

    @allure.step('Get {locator}')
    def get_field(self, locator):
        element = self.driver.find_element(*locator)
        logger.info(f'Get value attribute from {locator}')
        return element.get_attribute("value")

    @allure.step('Clicking {locator}')
    def click(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            logger.info(f'Clicking on {locator}. Try {i + 1} of {CLICK_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                self.scroll_to(element)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
