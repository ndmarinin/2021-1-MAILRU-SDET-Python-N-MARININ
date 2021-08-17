import logging

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os.path
import pathlib
from typing import Final

IMPLICITLY_WAIT: Final[int] = 30
GECKODRIVER_PATH: Final[str] = os.path.join(pathlib.Path(__file__).parent.absolute(), "geckodriver")

@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    selenoid = request.config.getoption('--selenoid_host')
    return {'url': url, 'selenoid_host': selenoid}


def pytest_addoption(parser):
    parser.addoption('--url', default='http://myapp:8080')
    parser.addoption('--selenoid_host', default='solenoid:4444')
    parser.addoption('--browser', default='chrome')



@pytest.fixture(scope='function')
def driver(request) -> WebDriver:
    """
    Generate the Selenium driver that will be used by the tests
    :param request:
    :return: a callable that generates the driverSelenium WebDriver instance
    """
    browser = request.config.getoption('--browser')
    capabilities = {
        "browserName": browser,
    }

    driver: WebDriver
    driver = webdriver.Remote(
        "http://solenoid:4444/wd/hub".format(
        ), capabilities
    )
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.get("http://myapp:8080")
    yield driver
    driver.close()


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join("test_dir", 'test.log')

    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def test_dir(request):
    base_test_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))) + 'tests'
    config.base_test_dir = base_test_dir

    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(base_test_dir, test_name)


    #test_dir = os.path.join(request.config.base_test_dir, request._pyfuncitem.nodeid)

    try:
        os.makedirs(test_dir)
    except OSError:
        pass
    try:
        os.makedirs(base_test_dir)
    except OSError:
        pass

    return test_dir