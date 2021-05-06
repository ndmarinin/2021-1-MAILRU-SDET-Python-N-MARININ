import os

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

    def get_file_version(self):
        dir = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))) + '\\stuff\\'
        file_name = os.listdir(dir)[0]
        return file_name[10:16]