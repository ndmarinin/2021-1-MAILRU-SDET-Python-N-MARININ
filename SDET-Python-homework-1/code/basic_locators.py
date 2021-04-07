from selenium.webdriver.common.by import By

LOGIN_MENU = (By.XPATH, '//div[contains(text(), "Войти")]')

EMAIL = (By.NAME, 'email')
PASS = (By.NAME, 'password')

LOGIN_BUTTON = (By.XPATH, '//div[contains(@class, "authForm-module-button")]') #Два элемента с текстов войти, поэтому так
PROFILE = (By.XPATH, '//div[contains(@class, "right-module-userNameWrap")]') #Кнопка профиля
FIO_FIELD = (By.XPATH, '//div[@data-name="fio"]/div/input')
PHONE_FIELD = (By.XPATH, '//div[@data-name="phone"]/div/input')
HEADER = (By.XPATH, '//div[contains(@class, "responseHead-module-wrapper")]')

MAIL_FIELD = (By.XPATH, '//div[@class="js-additional-email profile__list__row__input"]/div/div/input')

SAVE_BUTTON =(By.XPATH, '//div[@class="button__text"]')


TEXT_EMAIL = (By.NAME, 'email')
TEXT_PASS = (By.NAME, 'password')
LOGOUT = (By.XPATH, "//a[@href='/logout']")
LOGOUT_BUTTON = (By.XPATH, '//div[contains(@class, "responseHead-module-button")]')
EDIT_PROFILE = (By.XPATH, "//a[@href='/profile']")
BILLING = (By.XPATH, "//a[@href='/billing']")
STATS = (By.XPATH, "//a[@href='/statistics']")
