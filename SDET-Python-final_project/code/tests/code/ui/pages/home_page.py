from ui.locators.homePage_locators import HomePageLocators
from ui.pages.base_page import BasePage


class HomePage(BasePage):
    locators = HomePageLocators()

    def get_login_name(self):
        element = self.find(self.locators.LOGIN_NAME_LOCATOR, 10)
        return element.text
