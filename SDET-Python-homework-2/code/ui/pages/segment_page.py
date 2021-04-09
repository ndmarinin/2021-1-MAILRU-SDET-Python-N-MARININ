import os

import allure
import time

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentPageLocators


class Segment_Page(BasePage):
    locators = SegmentPageLocators


    @allure.step('Creating segment')
    def create_segment(self):
        self.click(self.locators.CREATE_SEGMENT, 5)
        self.click(self.locators.APPLICATIONS, 5)
        self.click(self.locators.CHECKBOX, 5)
        self.click(self.locators.ADD_SEGMENT, 5)
        name = self.get_field(self.locators.SEGMENT_NAME)
        self.click(self.locators.CREATE_SEGMENT, 5)
        time.sleep(3)
        return name

    @allure.step('Deleting segment {name}')
    def delete_segment(self, name):
        self.find((By.XPATH, f'//a[contains(text(), "{name}")]'), 5)
        element = self.find_elem((By.XPATH, f'//a[contains(text(), "{name}")]'))
        href = element.get_attribute('href')
        parts = str.split(href, '/')
        id = parts[len(parts) - 1]
        cell_id = self.driver.find_element_by_xpath(f'//span[contains(text(), "{id}")]/../input')
        cell_id.click()
        self.click(self.locators.ACTIONS, 5)
        self.click(self.locators.DELETE, 5)
        time.sleep(2)