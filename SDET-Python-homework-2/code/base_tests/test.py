import os
import time
import random
import string
from contextlib import contextmanager

import allure
import pytest

from base_tests.base import BaseCase

login = "vosaco7441@leonvero.com"
password = "vosaco7441"

class TestOne(BaseCase):



    @allure.epic('PyTest test')
    @allure.feature('UI tests')
    @allure.story('Log test')
    @allure.testcase('https://target.my.com')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Тест делает проверку создания компании")
    #@pytest.mark.skip
    @pytest.mark.ui
    def test_create_company(self, main_page_auth):
        lk_page = main_page_auth.go_to_dashboard()
        companypage = lk_page.go_to_companys()
        name = companypage.create_company()
        assert name in self.driver.page_source

    @pytest.mark.ui
    #@pytest.mark.skip
    def test_segment(self, main_page_auth):
        lk_page = main_page_auth.go_to_dashboard()
        segments = lk_page.go_to_segemnts()
        name = segments.create_segment()
        assert name in self.driver.page_source

    @pytest.mark.ui
    #@pytest.mark.skip
    def test_delete_segement(self, main_page_auth):
        lk_page = main_page_auth.go_to_dashboard()
        segments = lk_page.go_to_segemnts()
        name = segments.create_segment()
        segments.delete_segment(name)
        assert name not in self.driver.page_source


class TestFailure(BaseCase):

    @allure.epic('PyTest test')
    @allure.feature('UI tests')
    @allure.story('Log test 1')
    @allure.testcase('https://target.my.com')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Тест делает проверку логина с неправильными учетными данными")
    @pytest.mark.ui
    #@pytest.mark.skip
    def test_failure_1(self):
        self.main_page.enter_creds(login + random.choice(string.ascii_letters), password + random.choice(string.ascii_letters))
        assert 'Invalid login or password' in self.driver.page_source

    @allure.epic('PyTest test')
    @allure.feature('UI tests')
    @allure.story('Log test 2')
    @allure.testcase('https://target.my.com')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Тест делает проверку логина с неправильным форматом логина и пароля")
    @pytest.mark.ui
    #@pytest.mark.skip
    def test_failure_2(self):
        #self.driver.get('https://target.my.com')
        self.main_page.enter_creds(random.choice(string.ascii_letters), random.choice(string.ascii_letters))
        assert 'Введите email или телефон' in self.driver.page_source




