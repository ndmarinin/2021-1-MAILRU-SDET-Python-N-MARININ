from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import *

Base = declarative_base()


class test_users(Base):
    __tablename__ = 'test_users'
    __table_args = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False)
    access = Column(SMALLINT, nullable=True)
    active = Column(SMALLINT, nullable=True)
    start_active_time = Column(DATETIME, nullable=True)

    def __repr__(self):
        return f"<test_users(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'" \
               f")>"
