from mysql_utl import MysqlUtil


class CheckSQL:
    def __init__(self, db1, db2):
        self.__db1 = db1
        self.__db2 = db2
        self.__mysql_util1 = MysqlUtil(db1)
        self.__mysql_util2 = MysqlUtil(db2)

    def check_table(self):
        source_tables = self.__mysql_util1.get_tables()
        target_tables = self.__mysql_util2.get_tables()

        losing_tables = []
        for s_t in source_tables:
            table_name = s_t['table_name']
            if s_t in target_tables:
                self.check_column(table_name)
            else:
                # print('this schema does not has {0}'.format(table_name))
                losing_tables.append(table_name)

        if len(losing_tables) > 0:
            print('\nthis schema does not have these tables:')
            print(losing_tables)

    def check_column(self, table):
        losing_columns = []
        change_columns = []

        source_columns = self.__mysql_util1.get_columns(table)
        target_columns = self.__mysql_util2.get_columns(table)

        # print(source_columns)
        target_col_names = []
        for t_c in target_columns:
            target_col_names.append(t_c['column_name'])

        for s_c in source_columns:
            # print(s_c)
            column_name = s_c['column_name']
            if column_name in target_col_names:
                if s_c not in target_columns:
                    change_columns.append(column_name)
                    self.__mysql_util2.update_column(s_c, 'update', table)
            else:
                losing_columns.append(column_name)
                self.__mysql_util2.update_column(s_c, 'add', table)

        if len(losing_columns) > 0:
            print('this table {0} does not have these columns:'.format(table))
            print(losing_columns)

        if len(change_columns) > 0:
            print('this table {0} is different from target columns:'.format(table))
            print(change_columns)


check_sql = CheckSQL('mysql_source', 'mysql_target')
check_sql.check_table()
