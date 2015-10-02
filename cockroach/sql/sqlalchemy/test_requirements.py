from sqlalchemy.testing.requirements import SuiteRequirements
from sqlalchemy.testing import exclusions


# The SQLAlchemy Requirements class contains a set of boolean flags
# that control which tests are run for a dialect.
# TODO(bdarnell): turn on ("open") as many of these as we can.
# The trailing "#" marks the ones that I think we already support.
class Requirements(SuiteRequirements):
    create_table = exclusions.closed() #
    drop_table = exclusions.closed()  #

    foreign_keys = exclusions.closed()
    on_update_cascade = exclusions.closed()
    non_updating_cascade = exclusions.closed()
    deferrable_fks = exclusions.closed()
    on_update_or_deferrable_fks = exclusions.closed()
    self_referential_foreign_keys = exclusions.closed()
    foreign_key_ddl = exclusions.closed()
    named_constraints = exclusions.closed()

    subqueries = exclusions.closed() #
    offset = exclusions.closed() #
    bound_limit_offset = exclusions.closed() #
    boolean_col_expressions = exclusions.closed() #

    nullsordering = exclusions.closed()
    standalone_binds = exclusions.closed() #
    intersect = exclusions.closed()
    except_ = exclusions.closed()
    window_functions = exclusions.closed()
    autoincrement_insert = exclusions.closed()
    fetch_rows_post_commit = exclusions.closed() #
    empty_inserts = exclusions.closed() #
    insert_from_select = exclusions.closed()
    returning = exclusions.closed()
    duplicate_names_in_cursor_description = exclusions.closed() #
    denormalizd_names = exclusions.closed()
    multivalues_inserts = exclusions.closed() #
    implements_get_lastrowid = exclusions.closed()
    emulated_lastrowid = exclusions.closed()
    dbapi_lastrowid = exclusions.closed()
    views = exclusions.closed()
    schemas = exclusions.closed()
    sequences = exclusions.closed()
    sequences_optional = exclusions.closed()

    reflects_pk_names = exclusions.closed() #
    table_reflection = exclusions.closed() #
    view_column_reflection = exclusions.closed()
    view_reflection = exclusions.closed()
    schema_reflection = exclusions.closed()
    primary_key_constraint_reflection = exclusions.closed() #
    foreign_key_constraint_reflection = exclusions.closed() #
    temp_table_reflection = exclusions.closed()
    temp_table_names = exclusions.closed()
    temporary_tables = exclusions.closed()
    temporary_views = exclusions.closed()
    index_reflection = exclusions.closed() #
    unique_constraint_reflection = exclusions.closed() #

    duplicate_key_raises_integrity_error = exclusions.closed()
    unbounded_varchar = exclusions.closed() #
    unicode_data = exclusions.closed() #
    unicode_ddl = exclusions.closed() #
    datetime_literals = exclusions.closed() #
    datetime = exclusions.closed() #
    datetime_microseconds = exclusions.closed() #
    datetime_historic = exclusions.closed() #
    date = exclusions.closed() #
    date_coerces_from_datetime = exclusions.closed() #
    date_historic = exclusions.closed() #
    time = exclusions.closed() #
    time_microseconds = exclusions.closed() #
    binary_comparisons = exclusions.closed() #
    binary_literals = exclusions.closed() #
    precision_numerics_general = exclusions.closed()
    precision_numerics_enotation_small = exclusions.closed()
    precision_numerics_enotation_large = exclusions.closed()
    precision_numerics_many_significant_digits = exclusions.closed()
    precision_numerics_retains_significant_digits = exclusions.closed()
    precisions_generic_float_type = exclusions.closed() #
    floats_to_four_decimals = exclusions.closed() #
    fetch_null_numeric = exclusions.closed() #
    text_type = exclusions.closed() #
    empty_strings_varchar = exclusions.closed() #
    empty_strings_text = exclusions.closed() #

    selectone = exclusions.closed() #
    savepoints = exclusions.closed()
    two_phase_transactions = exclusions.closed()
    update_from = exclusions.closed()
    update_where_target_in_subquery = exclusions.closed() #
    mod_operator_as_percent_sign = exclusions.closed() #
    percent_schema_names = exclusions.closed() #
    order_by_label_with_expression = exclusions.closed() #
    unicode_connections = exclusions.closed() #
    graceful_disconnects = exclusions.closed() #
