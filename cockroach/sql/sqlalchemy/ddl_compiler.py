import sqlalchemy.sql.compiler


class DDLCompiler(sqlalchemy.sql.compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs):
        name = self.preparer.format_column(column)
        typespec = self.dialect.type_compiler.process(
            column.type, type_expression=column)
        if column.primary_key and column.autoincrement:
            default = "DEFAULT experimental_unique_int()"
        else:
            default = self.get_column_default_string(column)
        if default is None:
            return "%s %s" % (name, typespec)
        else:
            return "%s %s %s" % (name, typespec, default)
