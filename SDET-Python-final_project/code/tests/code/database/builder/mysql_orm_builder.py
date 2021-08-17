from database.client.mysql_orm_client import SQLOrmClient
from database.models.user import *

class MySqlOrmBuilder(object):
    def __init__(self, client: SQLOrmClient):
        self.client = client
        self.engine = self.client.connection.engine

    def add_user(self, username, email, password, access, active):
        test_user = test_users(
            username=username,
            email=email,
            password=password,
            access=access,
            active=active
        )

        self.client.session.add(test_user)
        self.client.session.commit()
        return test_user

    def del_user(self, username):
        self.client.session.query(test_users).filter_by(username=username).delete(synchronize_session='fetch')
        self.client.session.commit()

    def get_user(self, username):
        self.client.session.commit()
        return self.client.session.query(test_users).filter_by(username=username).first()
