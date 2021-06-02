import pytest
import settings
from mock.flask_mock import SURNAME_DATA
from base.base import Base

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


class Test:

    def test_add_get_user(self):
        status1, data1 = Base.post_add_user(self, name='Ilya')
        assert status1 == 201
        status2, data2 = Base.get_user(self, name='Ilya')
        assert status2 == 200
        assert data1['user_id'] == data2['user_id']

    def test_get_non_existent_user(self):
        status1, data1 = Base.get_user(self, name='dnsfndksfnkjsdnfjkdsjkfnsd')
        assert status1 == 404

    def test_add_existent_user(self):
        status1, data1 = Base.post_add_user(self, name='Ilya')
        assert status1 == 201
        status2, data2 = Base.post_add_user(self, name='Ilya')
        assert status2 == 400

    def test_get_age(self):
        status1, data1 = Base.post_add_user(self, name='Vasya')
        assert status1 == 201
        status2, data2 = Base.get_user(self, name='Vasya')
        assert status2 == 200
        assert isinstance(data2['age'], int)
        assert 0 <= data2['age'] <= 100

    def test_has_surname(self):
        SURNAME_DATA['Olya'] = 'Zaitceva'
        status1, data1 = Base.post_add_user(self, name='Olya')
        assert status1 == 201
        status2, data2 = Base.get_user(self, name='Olya')
        assert status2 == 200
        assert data2['surname'] == 'Zaitceva'

    def test_has_not_surname(self):
        status1, data1 = Base.post_add_user(self, name='Sveta')
        assert status1 == 201
        status2, data2 = Base.get_user(self, name='Sveta')
        assert status2 == 200
        assert data2['surname'] is None

    def test_delete_user(self):
        status1, data1 = Base.post_add_user(self, name='Oleg')
        assert status1 == 201
        status2, data2 = Base.delete_user(self, name='Oleg')
        assert status2 == 200
        status3, data3 = Base.get_user(self, name='Oleg')
        assert status3 == 404

    def test_update_user(self):
        SURNAME_DATA['Petr'] = 'Ivanov'
        status1, data1 = Base.post_add_user(self, name='Petr')
        assert status1 == 201
        status2, data2 = Base.put_update_user(self, name='Petr', surname='Kovalskiy')
        assert status2 == 200
        status3, data3 = Base.get_user(self, name='Petr')
        assert status3 == 200
        assert data3['surname'] == 'Kovalskiy'

    def test_no_delete_user(self):
        status1, data1 = Base.delete_user(self, name='qwertyuiop')
        assert status1 == 404

    def test_update_no_user(self):
        status1, data1 = Base.put_update_user(self, name='qwerty', surname='ytrewq')
        assert status1 == 404

    def test_delete_surname(self):
        status1, data1 = Base.delete_surname(self, name='Petr')
        assert status1 == 200
        status2, data2 = Base.get_user(self, name='Petr')
        assert data2['surname'] is None

    def test_shutdown(self):
        status1, data1 = Base.shutdown_server(self)
        assert 200 == status1
        status2, data2 = Base.get_user(self, name='Petr')
        assert data2['surname'] is None
