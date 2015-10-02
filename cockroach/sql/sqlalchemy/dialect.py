from sqlalchemy.engine.interfaces import Dialect
from sqlalchemy.engine.default import DefaultDialect

from cockroach.sql import driver
from .ddl_compiler import DDLCompiler
from .type_compiler import TypeCompiler


class CockroachDialect(DefaultDialect):
    driver = driver
    ddl_compiler = DDLCompiler
    type_compiler = TypeCompiler

    supports_native_boolean = True

    @classmethod
    def dbapi(cls):
        return driver

    def has_table(self, conn, table, schema=None):
        for row in conn.execute("SHOW TABLES"):
            if row[0] == table:
                return True
        return False
