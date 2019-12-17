import db.mysql
import logger.logger as log


def app_init():
    '''
    执行应用初始化
    :return:
    '''
    db.mysql.mysql_db.connect()
    log.info('app init finish')
