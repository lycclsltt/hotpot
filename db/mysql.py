# coding=utf-8

from agileutil.db4 import PoolDB
from decouple import config
import os

#兼容rc环境
mysqlDbHost = config('DB_HOST')
if 'CONTAINER_ENV' in os.environ:
    if os.environ['CONTAINER_ENV'] == 'rc':
        mysqlDbHost = os.environ['CONTAINER_ENV'] + '.' + mysqlDbHost

#初始化连接池最小连接数
minConnNum = 10
if config('DB_POOL_MIN_CONNECTION') != '':
    minConnNum = int(config('DB_POOL_MIN_CONNECTION'))

#初始化连接超时
dbConnectTimeout = 10
if config('DB_POOL_CONNECT_TIMEOUT') != '':
    dbConnectTimeout = int(config('DB_POOL_CONNECT_TIMEOUT'))

#初始化读取超时
dbReadTimeout = 10
if config('DB_POOL_READ_TIMEOUT') != '':
    dbReadTimeout = int(config('DB_POOL_READ_TIMEOUT'))

#初始化端口
dbPort = 3306
if config('DB_PORT') != '':
    dbPort = int(config('DB_PORT'))

mysql_db = None
if mysql_db == None:
    mysql_db = PoolDB(mysqlDbHost,
                      dbPort,
                      config('DB_USER'),
                      config('DB_PWD'),
                      config('DB_NAME'),
                      min_conn_num=minConnNum,
                      connect_timeout=dbConnectTimeout,
                      read_timeout=dbReadTimeout)
    print('mysql db host:', mysqlDbHost)


def query(sql):
    return mysql_db.query(sql)


def update(sql):
    return mysql_db.update(sql)


def lastrowid():
    return mysql_db.lastrowid()
