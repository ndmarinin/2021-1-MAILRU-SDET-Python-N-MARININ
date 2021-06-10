from selenium.webdriver.common.by import By


class HomePageLocators(object):
    HOME_MENU_LOCATOR = (By.XPATH, '//a[contains(text(),"HOME")]')
    PYTHON_MENU_LOCATOR = (By.XPATH, '//a[text()="Python"]')
    PYTHON_FLASK_MENU_LOCATOR = (By.XPATH, '//a[text()="About Flask"]')
    PYTHON_HISTORY_MENU_LOCATOR = (By.XPATH, '//a[text()="Python history"]')


    LOG_VK_ID = (By.XPATH,  '//li[contains(text(),"VK ID:")]')
    LOG_USERNAME = (By.XPATH,  '//li[contains(text(),"Logged as")]')


    NETWORK_MENU_LOCATOR = (By.XPATH, '//a[contains(text(),"Network")]/..')
    NETWORK_WIRESHARK_NEWS_MENU_LOCATOR = (By.XPATH, '//a[contains(text(),"News")]')
    NETWORK_WIRESHARK_DOWNLOAD_MENU_LOCATOR = (By.XPATH, '//a[text()="Download"]')
    NETWORK_TCPDUMP_MENU_LOCATOR = (By.XPATH, '//a[contains(text(),"Examples ")]')

    API_HREF_LOCATOR = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    INTERNET_HREF_LOCATOR = (By.XPATH, '//a[@href="https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"]')
    SMTP_HREF_LOCATOR = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')

    LOGOUT_BUTTON_LOCATOR = (By.XPATH, '//*[@id="logout"]/a')
    LOGIN_NAME_LOCATOR = (By.XPATH, '//*[contains(text(), "Logged as")]')

    LINUX_MENU_LOCATOR = (By.XPATH, '//a[contains(text(),"Linux")]/..')
    CENTOS_BUTTON_LOCATOR = (By.XPATH, '//a[contains(text(),"Download Centos7")]')
