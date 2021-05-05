import pytest

from mysql.builder import MySQLBuilder
from mysql.models import Count, Methods, Error5xx, Error4xx, TopUrls
from tests.data import Make_data

class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)


class TestMysql(MySQLBase):

    data = Make_data()
    data.analyze()

    def make_count(self):
        self.mysql_builder.create_value(value=self.data.print_count())

    def make_method(self):
        met = self.data.print_method()
        for item in met:
            self.mysql_builder.create_method(method=item[0], count=item[1])

    def make_5xx(self):
        error5 = self.data.print_5xx()
        for item in error5:
            self.mysql_builder.create_5xx(ip=item[0], count=item[1])

    def make_4xx(self):
        error4 = self.data.print_4xx()
        for item in error4:
            self.mysql_builder.create_4xx(ip=item[3], url=item[0], status=item[1], size=item[2])

    def make_urls(self):
        urls = self.data.print_top10()
        for item in urls:
            self.mysql_builder.create_url(url=item[0], count=item[1])

    def get_count(self):
        count = self.mysql.session.query(Count).all()
        return count

    def get_method(self):
        method = self.mysql.session.query(Methods).all()
        return method

    def get_5xx(self):
        error = self.mysql.session.query(Error5xx).all()
        return error

    def get_4xx(self):
        error = self.mysql.session.query(Error4xx).all()
        return error

    def get_urls(self):
        urls = self.mysql.session.query(TopUrls).all()
        return urls


class TestRows(TestMysql):

    def test_count(self):
        self.make_count()
        data = self.get_count()
        assert len(data) == 1
        assert data[0].value == 199265

    def test_method(self):
        self.make_method()
        data = self.get_method()
        assert len(data) == 4
        assert data[0].method == "GET"

    def test_error5(self):
        self.make_5xx()
        data = self.get_5xx()
        assert len(data) == 5
        assert data[1].ip == "82.193.127.15"

    def test_error4(self):
        self.make_4xx()
        data = self.get_4xx()
        assert len(data) == 5
        assert data[2].id == 3

    def test_urls(self):
        self.make_urls()
        urls = self.get_urls()
        assert len(urls) == 10
        assert len(urls[5].url) > 10







