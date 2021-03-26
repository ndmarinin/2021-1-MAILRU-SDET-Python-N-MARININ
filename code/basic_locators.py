from selenium.webdriver.common.by import By

LOG_IN = (By.XPATH, '//div[contains(text(), "Войти")]')
EMAIL = (By.NAME, 'email')
PASS = (By.NAME, 'password')
LOGIN_BUTTON = (By.XPATH, '//div[@class="authForm-module-button-2G6lZu"]') #Два элемента с текстов войти, поэтому так
PROFILE = (By.XPATH, '//div[@class="right-module-userNameWrap-34ibLS"]') #Кнопка профиля
FIO_FIELD = (By.XPATH, '//div[@data-name="fio"]/div/input')
PHONE_FIELD = (By.XPATH, '//div[@data-name="phone"]/div/input')
MAIL_FIELD = (By.XPATH, '//div[@class="js-additional-email profile__list__row__input"]/div/div/input')

SAVE_BUTTON =(By.XPATH, '//div[@class="button__text"]')


TEXT_EMAIL = (By.NAME, 'email')
TEXT_PASS = (By.NAME, 'password')
LOGOUT = (By.XPATH, "//a[@href='/logout']")
EDIT_PROFILE = (By.XPATH, "//a[@href='/profile']")
BILLING = (By.XPATH, "//a[@href='/billing']")
STATS = (By.XPATH, "//a[@href='/statistics']")
