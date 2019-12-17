import db.mysql
import logger.logger as log


def app_init():
    '''
    这里做一些初始化，例如初始化MySQL连接池
    '''
    try:
        db.mysql.mysql_db.connect()
    except Exception as ex:
        pass
    log.info('app init finish')
