import pytest
from _pytest.fixtures import FixtureRequest

from database.builder.mysql_orm_builder import MySqlOrmBuilder
from database.client.mysql_orm_client import SQLOrmClient
from ui.pages.base_page import BasePage
from ui.pages.home_page import HomePage
from ui.pages.reg_page import RegPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config


        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.reg_page: RegPage = request.getfixturevalue('reg_page')
        self.home_page: HomePage = request.getfixturevalue('home_page')

        self.MySqlClient = SQLOrmClient(user='test_qa', password="qa_test", host='mysql', port=3306, db_name='test')
        self.MySqlBuilder = MySqlOrmBuilder(self.MySqlClient)
