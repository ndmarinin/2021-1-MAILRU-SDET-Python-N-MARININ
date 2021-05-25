from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Count(Base):
    __tablename__ = 'count'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Count(" \
               f"id='{self.id}'," \
               f"value='{self.value}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, primary_key=False, autoincrement=False)

class TopUrls(Base):
    __tablename__ = 'top10urls'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<top10urls(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), primary_key=False, autoincrement=False)
    count = Column(Integer, primary_key=False, autoincrement=False)

class Methods(Base):
    __tablename__ = 'methods'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<methods(" \
               f"id='{self.id}'," \
               f"method='{self.method}'," \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(500), primary_key=False, autoincrement=False)
    count = Column(Integer, primary_key=False, autoincrement=False)

class Error5xx(Base):
    __tablename__ = 'top5xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<top5xx(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}'," \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(500), primary_key=False, autoincrement=False)
    count = Column(Integer, primary_key=False, autoincrement=False)

class Error4xx(Base):
    __tablename__ = '5top4xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<5top4xx(" \
               f"id='{self.id}'," \
               f"url='{self.url}'," \
               f"status='{self.status}'," \
               f"size='{self.size}'," \
               f"ip='{self.ip}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), primary_key=False, autoincrement=False)
    status = Column(Integer, primary_key=False, autoincrement=False)
    size = Column(Integer, primary_key=False, autoincrement=False)
    ip = Column(String(500), primary_key=False, autoincrement=False)