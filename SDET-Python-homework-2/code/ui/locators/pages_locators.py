from selenium.webdriver.common.by import By


class BasePageLocators:
    BASE_PAGE_LOADED_LOCATOR = ''


class MainPageLocators(BasePageLocators):
    LOGIN_MENU = (By.XPATH, '//div[contains(text(), "Войти")]')
    EMAIL = (By.NAME, 'email')
    PASS = (By.NAME, 'password')
    LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]')  # Два элемента с текстов войти, поэтому так
    DASHBOARD = (By.XPATH, '//a[@href="/dashboard"]')

class CompanyPageLocators(BasePageLocators):
    COMPANY = (By.XPATH, '//a[@href="/campaign/new"]')
    CREATE_COMPANY = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')
    TRAFFIC = (By.XPATH, '//div[contains(text(), "Трафик")]')
    COMPANY_NAME = (By.XPATH, '//div[@class="input input_campaign-name input_with-close"]/div[2]/input')
    BANNER = (By.XPATH, '//span[contains(text(), "Баннер")]')
    UPLOAD = (By.XPATH, '//input[@accept=".jpg, .jpeg, .png, .gif"]')
    SAVE_IMAGE = (By.XPATH, '//input[@value="Сохранить изображение"]')
    SAVE = (By.XPATH, '//div[contains(text(), "Создать кампанию")]')
    URL = (By.XPATH, '//input[contains(@class, "mainUrl-module-searchInput")]')
    RELOAD = (By.XPATH, '//div[contains(@class, "icon-refresh")]' )
    COMPANY_TABLE = (By.XPATH, '//div[contains(@class, "main-module-TableWrapper")]')

class LKLocators(MainPageLocators):
    SEGMENT = (By.XPATH, '//a[@href="/segments"]')
    DASHBOARD = (By.XPATH, '//a[@href="/dashboard"]')

class SegmentPageLocators(BasePageLocators):

    ADD_SEGMENT = (By.XPATH, '//div[contains(text(), "Добавить сегмент")]')
    CREATE_SEGMENT = (By.XPATH, '//div[contains(text(), "Создать сегмент")]')
    SEGMENT_NAME = (By.XPATH, '//div[@class="input input_create-segment-form"]/div/input')
    ACTIONS = (By.XPATH, '//span[contains(text(), "Действия")]')
    DELETE = (By.XPATH, '//li[contains(text(), "Удалить")]')
    APPLICATIONS = (By.XPATH, '//div[contains(text(), "Приложения и игры в соцсетях")]')
    CHECKBOX = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox js-main-source-checkbox")]')
    SEGMENT_TEMPLATE = (By.XPATH, '//a[contains(text(), "{}")]')
    CELL_ID_TEMPLATE = (By.XPATH, '//span[contains(text(), "{}")]/../input')
    SEGMENT_TABLE = (By.XPATH, '//div[contains(@class, "main-module-TableWrapper")]')





