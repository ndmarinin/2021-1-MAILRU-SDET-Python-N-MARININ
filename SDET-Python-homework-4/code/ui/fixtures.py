import os
import shutil

import allure
import pytest
from appium import webdriver
from selenium import webdriver as wd
from ui.pages.base_page import BasePage
from ui.pages.search_page import SearchPage
from ui.pages.settings_page import SettingsPage
from ui import pages

from webdriver_manager.chrome import ChromeDriverManager
from ui.capability import capability_select


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)

@pytest.fixture
def settings_page(driver, config):
    page = get_page(config['device_os'], 'SettingsPage')
    return page(driver=driver, config=config)

@pytest.fixture
def main_page(driver, config):
    page = get_page(config['device_os'], 'MainPage')
    return page(driver=driver, config=config)


@pytest.fixture
def search_page(driver, config):
    page = get_page(config['device_os'], 'SearchPage')
    return page(driver=driver, config=config)



def get_page(device, page_class):
    page_class += 'ANDROID'
    page = getattr(pages, page_class, None)
    if page is None:
        raise Exception(f'No such page {page_class}')
    return page


def get_driver(appium_url):
    device_os = 'android'
    desired_caps = capability_select(device_os, '')
    driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
    return driver


@pytest.fixture(scope='function')
def driver(config):
    appium_url = config['appium']
    driver = get_driver(appium_url)
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)
        if config['device_os'] != 'android':
            browser_logfile = os.path.join(test_dir, 'browser.log')
            with open(browser_logfile, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

            with open(browser_logfile, 'r') as f:
                allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)