from selenium.webdriver.common.by import By


class BasePageLocators(object):
    LOGIN_INPUT_LOCATOR = (By.XPATH, '//*[@id="username"]')
    PASSWORD_INPUT_LOCATOR = (By.XPATH, '//*[@id="password"]')
    LOGIN_BUTTON_LOCATOR = (By.XPATH, '//*[@id="submit"]')
    CREATE_ACCOUNT_HREF_LOCATOR = (By.XPATH, '//a')