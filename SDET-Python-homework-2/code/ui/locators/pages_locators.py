from selenium.webdriver.common.by import By


class BasePageLocators:
    BASE_PAGE_LOADED_LOCATOR = ''


class MainPageLocators(BasePageLocators):
    LOGIN_MENU = (By.XPATH, '//div[contains(text(), "Войти")]')
    EMAIL = (By.NAME, 'email')
    PASS = (By.NAME, 'password')
    LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')  # Два элемента с текстов войти, поэтому так


class LKLocators(MainPageLocators):
    COMPANY = (By.XPATH, '//a[@href="/campaign/new"]')
    SEGMENT = (By.XPATH, '//a[@href="/segments"]')
    CREATE_COMPANY = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')
    ADD_SEGMENT = (By.XPATH, '//div[contains(text(), "Добавить сегмент")]')
    CREATE_SEGMENT = (By.XPATH, '//div[contains(text(), "Создать сегмент")]')
    TRAFFIC = (By.XPATH, '//div[contains(text(), "Трафик")]')
    URL = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    COMPANY_NAME = (By.XPATH, '//div[@class="input input_campaign-name input_with-close"]/div[2]/input')
    SEGMENT_NAME = (By.XPATH, '//div[@class="input input_create-segment-form"]/div/input')
    BANNER = (By.XPATH, '//span[contains(text(), "Баннер")]')
    ACTIONS = (By.XPATH, '//span[contains(text(), "Действия")]')
    DELETE = (By.XPATH, '//li[contains(text(), "Удалить")]')
    UPLOAD = (By.XPATH, '//input[@accept=".jpg, .jpeg, .png, .gif"]')
    SAVE_IMAGE = (By.XPATH, '//input[@value="Сохранить изображение"]')
    SAVE = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')
    APPLICATIONS = (By.XPATH, '//div[contains(text(), "Приложения и игры в соцсетях")]')
    CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox js-main-source-checkbox")]')
