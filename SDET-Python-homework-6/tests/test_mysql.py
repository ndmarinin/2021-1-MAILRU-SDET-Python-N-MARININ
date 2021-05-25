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
        return self.data.print_count()

    def make_method(self):
        met = self.data.print_method()
        for item in met:
            self.mysql_builder.create_method(method=item[0], count=item[1])
        return met

    def make_5xx(self):
        error5 = self.data.print_5xx()
        for item in error5:
            self.mysql_builder.create_5xx(ip=item[0], count=item[1])
        return error5

    def make_4xx(self):
        error4 = self.data.print_4xx()
        for item in error4:
            self.mysql_builder.create_4xx(ip=item[3], url=item[0], status=item[1], size=item[2])
        return error4

    def make_urls(self):
        urls = self.data.print_top10()
        for item in urls:
            self.mysql_builder.create_url(url=item[0], count=item[1])
        return urls

    def get_count(self):
        count = self.mysql.session.query(Count).all()
        return count

    def get_method(self):
        method = self.mysql.session.query(Methods).all()
        return self.parse_method(data=method)

    def get_5xx(self):
        error = self.mysql.session.query(Error5xx).all()
        return self.parse_5xx(error)

    def get_4xx(self):
        error = self.mysql.session.query(Error4xx).all()
        return self.parse_4xx(error)

    def get_urls(self):
        urls = self.mysql.session.query(TopUrls).all()
        return self.parse_url(urls)

    def parse_method(self, data):
        result = []
        for i in data:
            result.append([i.method, i.count])
        return result

    def parse_4xx(self, data):
        result = []
        for i in data:
            result.append([i.url, i.status, i.size, i.ip])
        return result

    def parse_5xx(self, data):
        result = []
        for i in data:
            result.append([i.ip, i.count])
        return result

    def parse_url(self, data):
        result = []
        for i in data:
            result.append([i.url, i.count])
        return result


class TestRows(TestMysql):

    def test_count(self):
        data1 = self.make_count()
        data2 = self.get_count()
        assert len(data2) == 1
        assert data1 == data2[0].value

    def test_method(self):
        data1 = self.make_method()
        data2 = self.get_method()
        assert len(data1) == len(data2)
        assert data1 == data2

    def test_error5(self):
        data1 = self.make_5xx()
        data2 = self.get_5xx()
        assert len(data1) == len(data2)
        assert data1 == data2

    def test_error4(self):
        data1 = self.make_4xx()
        data2 = self.get_4xx()
        assert len(data1) == len(data2)
        assert data1 == data2

    def test_urls(self):
        data1 = self.make_urls()
        data2 = self.get_urls()
        assert len(data1) == len(data2)
        assert data1 == data2
