# mysql_table_synchronizer
### 使用
1. 配置db.ini文件   
    mysql_source为基准数据库   
    mysql_target为对比数据库
2. 运行   
    `
    python3 start.py   
    `
    
### 注意
使用前请先安装python3及pymysql包   
不支持索引、外键，本项目会直接修改数据库，不要在生产环境中使用

### 说明
本项目使用python3开发，用来检测两个数据库表结构是否相同，并且修改表结构

在start.py文件中，is_execute设置为True会自动修改表结构，False不会修改
