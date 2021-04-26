import json
import time
from utils.decorators import wait
import pytest

from api.client import InvalidLoginException
from test_api.base import ApiBase
from utils.builder import Builder
email = 'vosaco7441@leonvero.com'

class NotFound(Exception):
    pass


class TestApi(ApiBase):

    @pytest.mark.api
    def test_valid_login(self, credentials):
        response = self.api_client.post_login(*credentials)
        assert email in response.text

    @pytest.mark.api
    def test_create_campagin(self, auth_user):
        campagin_name = Builder.create_text()
        id = self.api_client.post_create_company(campagin_name)
        wait(self.check_campany, id_camp=id, name=campagin_name, error=NotFound, timeout=20)
        self.api_client.post_delete_company(id)

    @pytest.mark.api
    def test_create_segment(self, auth_user):
        segment_name = Builder.create_text()
        id = self.api_client.post_create_segment(segment_name)
        wait(self.check_segment, id=id, name=segment_name, error=NotFound, timeout=10)


    @pytest.mark.api
    def test_delete_segment(self, auth_user):
        segment_name = Builder.create_text()
        id = self.api_client.post_create_segment(segment_name)
        self.api_client.post_delete_segment(id)
        with pytest.raises(TimeoutError):
            wait(self.check_segment, id=id, name=segment_name, error=NotFound, timeout=10)

    def check_segment(self, id, name):
        all_segments = self.api_client.get_segments()['items']
        my_segment = [s for s in all_segments if s['id'] == id]

        if not my_segment:
            raise NotFound('Empty result')
        assert len(my_segment) == 1, 'More than 1 segment with this id found'
        my_segment = my_segment[0]
        assert my_segment['name'] == name, 'Name of found degment differs'

    def check_campany(self, id_camp, name):
        all_campagins = self.api_client.get_campagins()['items']
        ext = []
        for s in all_campagins:
            new_id = int(s['id'])
            if new_id == int(id_camp):
                ext.append(s)

        if len(ext) == 0:
            raise NotFound('Empty result')
        assert len(ext) == 1, 'More than 1 segment with this id found'
        my_campagin = ext[0]
        assert my_campagin['name'] == name, 'Name of found degment differs'