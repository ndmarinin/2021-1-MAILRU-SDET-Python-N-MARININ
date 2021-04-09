import os

import allure
import time

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import LKLocators


class LK_Page(BasePage):
    locators = LKLocators()

    @allure.step('Creating company')
    def create_company(self):
        time.sleep(2)
        self.click(self.locators.CREATE_COMPANY, 5)
        self.click(self.locators.TRAFFIC, 5)
        self.enter_data(self.locators.URL, "https://mail.ru/")
        time.sleep(3)
        name = self.get_field(self.locators.COMPANY_NAME)
        self.click(self.locators.BANNER, 5)
        time.sleep(3)
        file_path = self.file_path()
        self.send_data(self.locators.UPLOAD, file_path)
        self.click(self.locators.SAVE_IMAGE, 5)
        self.click(self.locators.SAVE, 5)
        time.sleep(7)

        self.wait()
        return name

    @allure.step('Creating segment')
    def create_segment(self):
        self.click(self.locators.SEGMENT, 5)
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
        self.click(self.locators.SEGMENT, 5)
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
