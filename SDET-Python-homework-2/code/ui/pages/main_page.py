import allure

from ui.pages.base_page import BasePage
from ui.pages.lk_page import LK_Page
from ui.locators.pages_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step('Enter creds')
    def enter_creds(self, login, password):
        self.click(self.locators.LOGIN_MENU, 5)
        self.enter_data(self.locators.EMAIL, login)
        self.enter_data(self.locators.PASS, password)
        self.click(self.locators.LOGIN_BUTTON, 5)

    @allure.step('Go to dashboard')
    def go_to_dashboard(self):
        self.click(self.locators.DASHBOARD)
        return LK_Page(self.driver)
