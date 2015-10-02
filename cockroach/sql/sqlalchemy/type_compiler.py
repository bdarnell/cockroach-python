import sqlalchemy.sql.compiler


class TypeCompiler(sqlalchemy.sql.compiler.GenericTypeCompiler):
    def visit_DATETIME(self, type_, **kw):
        return "TIMESTAMP"

    def visit_DECIMAL(self, type_, **kw):
        # TODO(bdarnell): replace with DECIMAL when we have it.
        return "FLOAT"

    visit_NUMERIC = visit_DECIMAL
