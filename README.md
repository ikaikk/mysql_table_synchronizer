# mysql_table_synchronizer
用来检测两个数据库表结构是否相同，并且修改表结构

本项目使用python3开发

在start.py文件中，is_execute设置为True会自动修改表结构，False不会修改

注意：不支持索引、外键，本项目会直接修改数据库，不要在生产环境中使用