import allure

from ui.pages.base_page import BasePage
from ui.locators.locators_android import SettingsPageANDROIDLocators


class SettingsPage(BasePage):

    def go_to_about(self):
        pass

    def get_version(self):
        pass

    def get_copyright(self):
        pass

    def go_to_menu(self):
        pass

    def go_back(self):
        pass


class SettingsPageANDROID(SettingsPage):
    locators = SettingsPageANDROIDLocators()

    @allure.step("переход в раздел о программе")
    def go_to_about(self):
        self.click_for_android(self.locators.MENU)
        self.swipe_to_element(self.locators.ABOUT, max_swipes=2)
        self.click_for_android(self.locators.ABOUT)

    @allure.step("Поулчение версии программы")
    def get_version(self):
        text = self.get_value(self.locators.VERISON)
        text = text.split(' ')
        return text[1]

    @allure.step("Поулчение копрайта")
    def get_copyright(self):
        return self.get_value(self.locators.COPY_RIGHT)

    @allure.step("Переход в новости")
    def go_to_menu(self):
        self.click_for_android(self.locators.MENU)
        self.swipe_to_element(self.locators.NEWS, max_swipes=2)
        self.click_for_android(self.locators.NEWS)
        self.click_for_android(self.locators.VESTI)
        elem = self.find(self.locators.CHECK)
        assert elem is not None
        self.click_for_android(self.locators.BACK)
        elem = self.find_elements(self.locators.BACK, 0)
        elem.click()

