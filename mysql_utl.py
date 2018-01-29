import pymysql

from configer_util import ConfigUtil


class MysqlUtil:

    def __init__(self, db):
        config = ConfigUtil('./db.ini')
        self.__schema = config.get(db, 'db.schema')
        self.__url = config.get(db, 'db.url')
        self.__user = config.get(db, 'db.user')
        self.__password = config.get(db, 'db.password')
        self.__port = int(config.get(db, 'db.port'))
        self.__config = {
            'host': self.__url,
            'port': self.__port,
            'user': self.__user,
            'password': self.__password,
            'db': self.__schema,
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }

    def get_connection(self):
        return pymysql.connect(**self.__config)

    def execute(self, sql, params=None):
        conn = self.get_connection()
        count = 0

        try:
            with conn.cursor() as cursor:
                count = cursor.execute(sql, params)
            conn.commit()
        except Exception as ex:
            conn.rollback()
            print(ex)
        finally:
            conn.close()
        return count

    def query_one(self, sql):
        conn = self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        return result

    def query_multi(self, sql, params=None):
        conn = self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        return result

    def get_tables(self):
        sql = 'select table_name, engine, table_collation, table_comment from information_schema.tables where ' \
              'table_schema = %s and table_type = \'{0}\''.format('BASE TABLE')
        params = self.__schema
        return self.query_multi(sql, params)

    def get_columns(self, table_name):
        sql = 'select column_name, is_nullable, column_key, ' \
              'column_default, column_comment, column_type ' \
              'from information_schema.columns where table_schema = %s and table_name = %s'
        params = (self.__schema, table_name)
        return self.query_multi(sql, params)

    def update_column(self, column, modify_type, table_name, is_execute):
        column_name = column['column_name']
        is_nullable = column['is_nullable']
        column_type = column['column_type']
        column_default = column['column_default']
        column_comment = column['column_comment']

        sql = 'alter table {0} '.format(table_name)
        if 'add' == modify_type:
            sql += 'add column {column} '.format(column=column_name)
        elif 'update' == modify_type:
            sql += 'change column {column} {column} '.format(column=column_name)
        else:
            sql += 'drop column {column}'.format(column=column_name)

        if 'drop' != modify_type:
            sql += '{column_type} '.format(column_type=column_type)

            if 'YES' == is_nullable:
                sql += 'null '
            else:
                sql += 'not null '

            if column_default is not None:
                sql += 'default {default} '.format(default=column_default)

            if column_comment is not None:
                sql += 'comment \'{comment}\''.format(comment=column_comment)

        print(sql)
        if is_execute:
            self.execute(sql)

    def generate_create_sql(self, table_name):
        sql = 'show create table {0}'.format(table_name)
        result = self.query_one(sql)
        return result['Create Table']

    def create_table(self, sql, is_execute):
        print(sql)
        print('\n')
        if is_execute:
            self.execute(sql)
