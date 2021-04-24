import time
from utils.decorators import wait
import pytest

from api.client import InvalidLoginException
from test_api.base import ApiBase
from utils.builder import Builder
email = 'vosaco7441@leonvero.com'

class TestApi(ApiBase):

    @pytest.mark.api
    def test_valid_login(self, credentials):
        response = self.api_client.post_login(*credentials)
        assert email in response.text

    @pytest.mark.api
    def test_create_campagin(self, auth_user):
        campagin_name = Builder.create_text()
        id = self.api_client.post_create_company(campagin_name)
        wait(self.api_client.check(id), error=AssertionError, timeout=10)
        self.api_client.post_delete_company(id)

    @pytest.mark.api
    def test_create_segment(self, auth_user):
        segment_name = Builder.create_text()
        id = self.api_client.post_create_segment(segment_name)
        assert str(id) in self.api_client.get_segments().text

    @pytest.mark.api
    def test_delete_segment(self, auth_user):
        segment_name = Builder.create_text()
        id = self.api_client.post_create_segment(segment_name)
        self.api_client.post_delete_segment(id)
        response = self.api_client.get_segments()
        assert str(id) not in response.text