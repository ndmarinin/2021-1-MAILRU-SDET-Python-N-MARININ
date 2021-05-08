import time

from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage
from ui.locators.locators_android import SearchPageANDROIDLocators
import allure


class SearchPage(BasePage):

    def send_text_to_search_field_and_click_to_element(self, text, desc):
        pass

    def enter_value_in_search_field(self, text):
        pass

    def enter_value_in_search_field_and_click_on_first(self, text):
        pass

    def enter_value_in_field(self, text):
        pass

    def get_card(self):
        pass

    def go_to_step(self):
        pass

    def get_dialog(self):
        pass



class SearchPageANDROID(SearchPage):
    locators = SearchPageANDROIDLocators()

    @allure.step("Вводим значение в поле поиска")
    def enter_value_in_field(self, text):
        self.click_for_android(self.locators.KEYBOARD)
        self.find(self.locators.INPUT_TEXT).send_keys(text)
        self.driver.hide_keyboard()
        self.click_for_android(self.locators.SEARCH_BUTTON)


    def get_card(self):
        elemnt = self.find(self.locators.CARD)
        return elemnt.text

    def get_dialog(self):
        element = self.find_elements(self.locators.DIALOG_ITEM, 1)
        return element.text




    def go_to_step(self):
        self.click_for_android(self.locators.NUMBERS)
        self.swipe_up()
        self.swipe_up()
        elem = self.find(self.locators.CARD_TITLE)
        return elem.text