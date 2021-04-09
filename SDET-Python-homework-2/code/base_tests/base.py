import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.lk_page import LK_Page
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


        self.logger.debug('Initial setup done!')
    @pytest.fixture()
    def driver_auth(self, driver, config):
        self.driver = driver
        self.config = config
        self.main_page.enter_creds(login, password)