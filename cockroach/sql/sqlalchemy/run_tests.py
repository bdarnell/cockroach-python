#!/usr/bin/env python

from sqlalchemy.dialects import registry
from sqlalchemy.testing import runner

registry.register("cockroach", "cockroach.sql.sqlalchemy", "CockroachDialect")

if __name__ == "__main__":
    runner.main()
