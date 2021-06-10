import random
import string

from ui.locators.regPage_locators import RegPageLocators
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage


class RegPage(BasePage):

    locators = RegPageLocators()

    def register_user(self, username, email, password, mismatch=False):
        letters = string.ascii_lowercase
        self.enter_data(self.locators.USERNAME_INPUT_LOCATOR, username)
        self.enter_data(self.locators.EMAIL_INPUT_LOCATOR, email)
        self.enter_data(self.locators.PASSWORD_INPUT_LOCATOR, password)
        if mismatch:
            password = password.join(random.choice(letters) for i in range(1))
            self.enter_data(self.locators.CONFIRM_PASS_INPUT_LOCATOR, password)
        else:
            self.enter_data(self.locators.CONFIRM_PASS_INPUT_LOCATOR, password)
        self.click(self.locators.TERM_CHECKBOX_LOCATOR, 5)
        self.click(self.locators.SUBMIT_BUTTON_LOCATOR, 5)
        return HomePage(self.driver)
