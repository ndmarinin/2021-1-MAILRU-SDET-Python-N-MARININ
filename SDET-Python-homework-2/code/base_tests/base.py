import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.lk_page import LK_Page
from ui.pages.company_page import Company_Page
from ui.pages.segment_page import Segment_Page
login = "vosaco7441@leonvero.com"
password = "vosaco7441"

class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.lk_page: LK_Page = request.getfixturevalue('lk_page')
        self.company_page: Company_Page = request.getfixturevalue('company_page')
        self.segment_page: Segment_Page = request.getfixturevalue('segment_page')

        self.logger.debug('Initial setup done!')


