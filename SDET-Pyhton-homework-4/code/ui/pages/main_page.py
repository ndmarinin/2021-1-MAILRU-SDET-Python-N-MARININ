from ui.pages.base_page import BasePage
from ui.locators.locators_android import MainPageANDROIDLocators
import allure


class MainPage(BasePage):

    def skip_start_window(self):
        pass


class MainPageANDROID(MainPage):
    locators = MainPageANDROIDLocators()

    @allure.step("Пропускаем стартовое окно")
    def skip_start_window(self):
        self.click_for_android(self.locators.ALLOW_BUTTON)
        self.click_for_android(self.locators.ALLOW_BUTTON)
