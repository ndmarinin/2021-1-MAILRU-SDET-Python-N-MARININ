from faker import Faker

from mysql.models import  TopUrls, Error5xx, Error4xx, Methods, Count

fake = Faker()


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_value(self, value=None):
        if not value is None:
            result = Count(
                value=value
            )
            self.client.session.add(result)
            self.client.session.commit()
            return value



    def create_url(self, url=None, count=None):
        if not url is None and not count is None:
            string = TopUrls(
                url=url,
                count=count
            )
            self.client.session.add(string)
            self.client.session.commit()
            return string

    def create_5xx(self, ip=None, count=None):
        if not ip is None and not count is None:
            error = Error5xx(
                ip=ip,
                count=count
            )
            self.client.session.add(error)
            self.client.session.commit()
            return error

    def create_4xx(self, ip=None, url=None, status=None, size=None,):
        if not ip is None and not url is None and not status is None and not size is None:
            error = Error4xx(
                ip=ip,
                url=url,
                status=status,
                size=size
            )
            self.client.session.add(error)
            self.client.session.commit()
            return error

    def create_method(self, method=None, count=None):
        if not method is None and not count is None:
            method = Methods(
                method=method,
                count=count
            )
            self.client.session.add(method)
            self.client.session.commit()
            return method

