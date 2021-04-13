import os

import allure
import time

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import SegmentPageLocators


class Segment_Page(BasePage):
    locators = SegmentPageLocators


    @allure.step('Creating segment')
    def create_segment(self, name):
        self.click(self.locators.CREATE_SEGMENT, 5)
        self.click(self.locators.APPLICATIONS, 5)
        self.click(self.locators.CHECKBOX, 5)
        self.click(self.locators.ADD_SEGMENT, 5)
        self.enter_data(self.locators.SEGMENT_NAME, name)
        self.click(self.locators.CREATE_SEGMENT, 5)
        self.click(self.locators.ACTIONS, 5)

    @allure.step('Deleting segment {name}')
    def delete_segment(self, name):
        locator_segement = (self.locators.SEGMENT_TEMPLATE[0], self.locators.SEGMENT_TEMPLATE[1].format(name))
        element = self.find_elem(locator_segement)
        href = element.get_attribute('href')
        parts = str.split(href, '/')
        id = parts[len(parts) - 1]
        locator_cell = (self.locators.CELL_ID_TEMPLATE[0], self.locators.CELL_ID_TEMPLATE[1].format(id))
        cell_id = self.find(locator_cell)
        cell_id.click()
        self.click(self.locators.ACTIONS, 5)
        self.click(self.locators.DELETE, 5)
        self.click(self.locators.ACTIONS, 5)