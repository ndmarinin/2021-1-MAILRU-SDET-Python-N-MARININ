import allure
import time

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import CompanyPageLocators


class Company_Page(BasePage):
    locators = CompanyPageLocators

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
        return name
