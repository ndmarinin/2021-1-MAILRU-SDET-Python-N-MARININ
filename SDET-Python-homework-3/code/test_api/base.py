import pytest
from selenium.webdriver.support.wait import WebDriverWait

from utils.builder import Builder

blog_id = 350


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, credentials):
        self.builder = Builder()
        self.api_client = api_client
        if self.authorize:
            self.api_client.post_login(*credentials)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)