from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy


class BasePageANDROIDLocators:
    pass



class MainPageANDROIDLocators(BasePageANDROIDLocators):
    ALLOW_BUTTON = (By.ID, 'com.android.packageinstaller:id/permission_allow_button')
    KEYBOARD = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    INPUT_TEXT = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    MENU = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')

class SettingsPageANDROIDLocators(BasePageANDROIDLocators):
    MENU = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    NEWS = 	(MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    VESTI = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'Вести FM')]")
    CHECK = (MobileBy.ID, 'ru.mail.search.electroscope:id/news_sources_item_selected')
    BACK = 	(MobileBy.CLASS_NAME, 'android.widget.ImageButton')
    ABOUT = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_about')
    VERISON = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_version')
    COPY_RIGHT = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_copyright')

class SearchPageANDROIDLocators(BasePageANDROIDLocators):
    KEYBOARD = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    INPUT_TEXT = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    SEARCH_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_send')
    CARD = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_content_text')
    CARD_TITLE = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    DIALOG_ITEM = (MobileBy.ID, 'ru.mail.search.electroscope:id/dialog_item')
    NUMBERS = (MobileBy.XPATH, "//android.widget.TextView[contains(@text, 'население россии')]")

