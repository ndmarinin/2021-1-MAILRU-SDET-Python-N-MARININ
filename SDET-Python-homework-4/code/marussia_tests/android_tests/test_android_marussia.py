import os
import time
import pytest
from marussia_tests.base import BaseCase



class TestMarussiaAndroid(BaseCase):

    @pytest.mark.AndroidUI
    def test_russia(self):
        self.search_page.enter_value_in_field('Russia')
        text = self.search_page.get_card()
        assert 'государство' in text
        text = self.search_page.go_to_step()
        assert '146' in text

    @pytest.mark.AndroidUI
    def test_calc(self):
        self.search_page.enter_value_in_field('2+2')
        time.sleep(3)
        text = self.search_page.get_dialog()
        assert '4' in text

    @pytest.mark.AndroidUI
    def test_news(self):
        self.settings_page.go_to_menu()
        self.search_page.enter_value_in_field('News')
        time.sleep(1)
        text = self.search_page.get_dialog()
        assert 'Вести' in text

    @pytest.mark.AndroidUI
    def test_settings(self):
        self.settings_page.go_to_about()
        text = self.settings_page.get_copyright()
        assert "Все права защищены" in text
        version = self.settings_page.get_version()
        assert version in self.get_file_version()

    def get_file_version(self):
        dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))) + '\\stuff\\'
        file_name = os.listdir(dir)[0]
        return file_name[10:16]










