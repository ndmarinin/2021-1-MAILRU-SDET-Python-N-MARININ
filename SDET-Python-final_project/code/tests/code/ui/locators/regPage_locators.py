from selenium.webdriver.common.by import By


class RegPageLocators(object):
    USERNAME_INPUT_LOCATOR = (By.XPATH, '//*[@id="username"]')
    EMAIL_INPUT_LOCATOR = (By.XPATH, '//*[@id="email"]')
    PASSWORD_INPUT_LOCATOR = (By.XPATH, '//*[@id="password"]')
    CONFIRM_PASS_INPUT_LOCATOR = (By.XPATH, '//*[@id="confirm"]')
    TERM_CHECKBOX_LOCATOR = (By.XPATH, '//*[@id="term"]')
    SUBMIT_BUTTON_LOCATOR = (By.XPATH, '//*[@id="submit"]')
    INVALID_EMAIL_LOCATOR = (By.XPATH, '//div[text()="Invalid email address"]')
    INVALID_NAME_LOCATOR = (By.XPATH, '//div[text()="Incorrect username length"]')
    SERVER_ERROR_LOCATOR = (By.XPATH, '//div[text()="Internal Server Error"]')
    PASSWORD_MISMATCH = (By.XPATH, '//div[text()="Passwords must match"]')
    EXIST_USER_LOCATOR = (By.XPATH, '//div[text()="User already exist"]')
