from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, Integer, String, Table, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy.orm import sessionmaker


tables = []


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    extra_payment = Column("extra_payment", Integer, nullable=False, default=0)


class Debts(Base):
    __tablename__ = "debts"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    amount = Column("amount", String, nullable=False)
    minimum_payment = Column("minimum_payment", String, nullable=False)
    name = Column("name", String, nullable=False)
    rate = Column("rate", String, nullable=False)
    month = Column("month", Integer, nullable=False)
    year = Column("year", Integer, nullable=False)


class debt_db(object):
    """Wrap the debt solution database and helper functions in a simple API"""

    def __init__(self, url, **kwargs):
        self._engine = create_engine(url, connect_args={"check_same_thread": False})
        self._connection = self._engine.connect()
        self._metadata = MetaData(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()

        self._users = Table(
            "users",
            self._metadata,
            Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
            Column("username", String, nullable=False),
            Column("password", String, nullable=False),
            Column("extra_payment", Integer, nullable=False),
        )
        self._debts = Table(
            "debts",
            self._metadata,
            Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
            Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
            Column("name", String, nullable=False),
            Column("amount", String, nullable=False),
            Column("minimum_payment", String, nullable=False),
            Column("rate", String, nullable=False),
            Column("month", Integer, nullable=False),
            Column("year", Integer, nullable=False),
        )
        tables.append(self._users)
        tables.append(self._debts)
        self._metadata.create_all(self._engine, tables)

    def create_user(self, username, password):
        user = Users(username=username, password=generate_password_hash(password))
        self._session.add(user)
        self._session.commit()
        return True

    def user_exists(self, username):
        query = select([self._users.columns.id]).where(
            self._users.columns.username == username
        )
        result_proxy = self._connection.execute(query)
        result_set = result_proxy.fetchall()
        if len(result_set) == 0:
            return False
        else:
            return True

    def get_user_id(self, username):
        query = select([self._users.columns.id]).where(
            self._users.columns.username == username
        )
        resultProxy = self._connection.execute(query)
        ResultSet = resultProxy.fetchall()
        return ResultSet[0].id

    def valid_credentials(self, username, password):
        if not self.user_exists(username):
            return False
        query = select([self._users.columns.password]).where(
            self._users.columns.username == username
        )
        result_proxy = self._connection.execute(query)
        result_set = result_proxy.fetchall()
        if check_password_hash(result_set[0].password, password):
            return True
        else:
            return False

    def create_debt(self, user_id, name, amount, rate, minimum_payment, month, year):
        debt = Debts(
            user_id=user_id,
            name=name,
            amount=amount,
            rate=rate,
            minimum_payment=minimum_payment,
            month=month,
            year=year,
        )
        self._session.add(debt)
        self._session.commit()

    def delete_debt(self, user_id, debt_id):
        query = delete(self._debts).where(
            self._debts.columns.user_id == user_id, self._debts.columns.id == debt_id
        )
        self._connection.execute(query)
        return True

    def get_debts_by_user_id(self, user_id):
        query = select([self._debts]).where(self._debts.columns.user_id == user_id)
        resultProxy = self._connection.execute(query)
        ResultSet = resultProxy.fetchall()
        debts = []
        for result in ResultSet:
            debt = Debts(
                id=result.id,
                user_id=user_id,
                name=result.name,
                amount=result.amount,
                rate=result.rate,
                minimum_payment=result.minimum_payment,
                month=result.month,
                year=result.year,
            )
            debts.append(debt)
        return debts

    def get_extra_payment_by_user_id(self, user_id):
        query = select([self._users.columns.extra_payment]).where(
            self._users.columns.id == user_id
        )
        resultProxy = self._connection.execute(query)
        ResultSet = resultProxy.fetchall()
        return int(ResultSet[0].extra_payment)

    def update_extra_payment(self, user_id, extra_payment):
        query = (
            update(self._users)
            .where(self._users.columns.id == user_id)
            .values(extra_payment=extra_payment)
        )
        self._connection.execute(query)
        return True
