import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.search_page import SearchPage
from ui.pages.settings_page import SettingsPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.search_page: SearchPage = request.getfixturevalue('search_page')
        self.settings_page: SettingsPage = request.getfixturevalue('settings_page')

        self.logger.debug('Initial setup done!')