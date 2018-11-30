from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import Table, Column, MetaData, select, testing, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing import fixtures
from sqlalchemy.types import Integer, DateTime
import threading

from cockroachdb.sqlalchemy import run_transaction

meta = MetaData()

# Plain table object for the core test.
account_table = Table('account', meta,
                      Column('acct', Integer, primary_key=True, autoincrement=False),
                      Column('balance', Integer))


# ORM class for the session test.
class Account(declarative_base()):
    __table__ = account_table


item_table = Table('item', meta,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('created', DateTime, server_default=func.now()))


class Item(declarative_base()):
    __table__ = item_table
    __mapper_args__ = {"eager_defaults": True}


class BaseRunTransactionTest(fixtures.TestBase):
    def setup_method(self, method):
        meta.create_all(testing.db)
        testing.db.execute(account_table.insert(), [dict(acct=1, balance=100),
                                                    dict(acct=2, balance=100)])

    def teardown_method(self, method):
        meta.drop_all(testing.db)

    def get_balances(self, conn):
        """Returns the balances of the two accounts as a list."""
        result = []
        query = (select([account_table.c.balance])
                 .where(account_table.c.acct.in_((1, 2)))
                 .order_by(account_table.c.acct))
        for row in conn.execute(query):
            result.append(row.balance)
        if len(result) != 2:
            raise Exception("Expected two balances; got %d", len(result))
        return result

    def run_parallel_transactions(self, callback):
        """Runs the callback in two parallel transactions.

        A barrier function is passed to the callback and should be run
        after the transaction has performed its first read. This
        synchronizes the two transactions to ensure that at least one
        of them must restart.
        """
        cv = threading.Condition()
        wait_count = [2]

        def worker():
            iters = [0]

            def barrier():
                iters[0] += 1
                if iters[0] == 1:
                    # If this is the first iteration, wait for the other txn to also read.
                    with cv:
                        wait_count[0] -= 1
                        cv.notifyAll()
                        while wait_count[0] > 0:
                            cv.wait()

            callback(barrier)
            return iters[0]

        with ThreadPoolExecutor(2) as executor:
            future1 = executor.submit(worker)
            future2 = executor.submit(worker)
            iters1 = future1.result()
            iters2 = future2.result()

        assert iters1 + iters2 > 2, ("expected at least one retry between the competing "
                                     "txns, got txn1=%d, txn2=%d" % (iters1, iters2))
        balances = self.get_balances(testing.db)
        assert balances == [100, 100], ("expected balances to be restored without error; "
                                        "got %s" % balances)


class RunTransactionCoreTest(BaseRunTransactionTest):
    def perform_transfer(self, conn, balances):
        if balances[0] > balances[1]:
            conn.execute(account_table.update().where(account_table.c.acct == 1)
                         .values(balance=account_table.c.balance-100))
            conn.execute(account_table.update().where(account_table.c.acct == 2)
                         .values(balance=account_table.c.balance+100))
        else:
            conn.execute(account_table.update().where(account_table.c.acct == 1)
                         .values(balance=account_table.c.balance+100))
            conn.execute(account_table.update().where(account_table.c.acct == 2)
                         .values(balance=account_table.c.balance-100))

    def test_run_transaction(self):
        def callback(barrier):
            def txn_body(conn):
                balances = self.get_balances(conn)
                barrier()
                self.perform_transfer(conn, balances)
            with testing.db.connect() as conn:
                run_transaction(conn, txn_body)
        self.run_parallel_transactions(callback)


class RunTransactionSessionTest(BaseRunTransactionTest):
    def test_run_transaction(self):
        def callback(barrier):
            Session = sessionmaker(testing.db)

            def txn_body(session):
                accounts = list(session.query(Account)
                                .filter(Account.acct.in_((1, 2)))
                                .order_by(Account.acct))
                barrier()
                if accounts[0].balance > accounts[1].balance:
                    accounts[0].balance -= 100
                    accounts[1].balance += 100
                else:
                    accounts[0].balance += 100
                    accounts[1].balance -= 100
            run_transaction(Session, txn_body)
        self.run_parallel_transactions(callback)


class InsertReturningTest(fixtures.TestBase):
    def setup_method(self, method):
        meta.create_all(testing.db)

    def teardown_method(self, method):
        meta.drop_all(testing.db)

    def test_insert_returning(self):
        # This test demonstrates the use of the INSERT RETURNING
        # clause with the ORM to return server-generated values from a
        # transaction. The expire_on_commit=False option is necessary
        # to make the objects valid after the transaction has
        # completed. The eager_defaults option (set above) is
        # necessary to handle fields other than the primary key (which
        # is always loaded eagerly)
        def txn_body(session):
            item = Item()
            session.add(item)
            return item

        Session = sessionmaker(testing.db, expire_on_commit=False)
        item = run_transaction(Session, txn_body)
        assert item.id is not None
        assert item.created is not None
