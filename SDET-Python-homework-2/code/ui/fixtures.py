import os
import shutil

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.lk_page import LK_Page
from ui.pages.company_page import Company_Page
from ui.pages.segment_page import Segment_Page

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

login = "vosaco7441@leonvero.com"
password = "vosaco7441"

class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)

@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)
@pytest.fixture
def lk_page(driver):
    return LK_Page(driver=driver)
@pytest.fixture
def company_page(driver):
    return Company_Page(driver=driver)
@pytest.fixture
def segment_page(driver):
    return Segment_Page(driver=driver)


@pytest.fixture(scope='function')
def main_page_auth(driver):
    main = MainPage(driver=driver)
    main.enter_creds(login, password)
    return main




def get_driver(browser_name, download_dir):
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})

        manager = ChromeDriverManager(version='latest')
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest', log_level=0)  # set log_level=0 to disable logging
        browser = webdriver.Firefox(executable_path=manager.install())
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')

    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']

    browser = get_driver(browser_name, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    url = config['url']

    browser = get_driver(request.param, download_dir=test_dir)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)