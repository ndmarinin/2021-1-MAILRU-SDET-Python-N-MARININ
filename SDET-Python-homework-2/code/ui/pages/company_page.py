import allure
import time

from ui.pages.base_page import BasePage
from ui.locators.pages_locators import CompanyPageLocators
from selenium.webdriver.support import expected_conditions as EC
from utils.decorators import wait


class Company_Page(BasePage):
    locators = CompanyPageLocators

    @allure.step('Creating company')
    def create_company(self, name):
        self.click(self.locators.CREATE_COMPANY, 5)
        self.click(self.locators.TRAFFIC, 10)
        self.enter_data(self.locators.URL, "https://mail.ru/")
        self.enter_data(self.locators.COMPANY_NAME, name)
        self.click(self.locators.BANNER, 5)
        file_path = self.file_path()
        self.send_data(self.locators.UPLOAD, file_path)
        self.click(self.locators.SAVE_IMAGE, 5)
        self.click(self.locators.SAVE, 5)
        self.click(self.locators.RELOAD, 5)
