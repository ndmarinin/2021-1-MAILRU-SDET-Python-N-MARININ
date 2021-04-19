import allure


from ui.pages.base_page import BasePage

from ui.pages.company_page import Company_Page
from ui.pages.segment_page import Segment_Page
from ui.locators.pages_locators import LKLocators


class LK_Page(BasePage):
    locators = LKLocators()

    @allure.step('Go to company')
    def go_to_companys(self):
        self.click(self.locators.DASHBOARD)
        return Company_Page(self.driver)

    @allure.step('Go to segments')
    def go_to_segemnts(self):
        self.click(self.locators.SEGMENT)
        return Segment_Page(self.driver)
