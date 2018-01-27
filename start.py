from check_sql import CheckSQL

is_execute = False
check_sql = CheckSQL('mysql_source', 'mysql_target')
check_sql.check_table(is_execute)
