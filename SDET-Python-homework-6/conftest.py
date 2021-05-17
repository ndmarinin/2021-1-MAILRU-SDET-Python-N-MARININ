import pytest

from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='toor', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='toor', db_name='TEST_SQL')
        mysql_client.recreate_db()
        mysql_client.connect()
        mysql_client.create_count()
        mysql_client.create_top10url()
        mysql_client.create_top_5xx()
        mysql_client.create_top_4xx()
        mysql_client.create_methods()
        mysql_client.connection.close()


