import db.mysql as mysql_db
import pymysql


class CommonModel:
    def __init__(self):
        self.tableName = ''

    def query(self, sql):
        rows = mysql_db.query(sql)
        if rows == None or len(rows) == 0:
            return []
        return rows

    def escapeString(self, string):
        return pymysql.escape_string(string)

    def update(self, sql):
        return mysql_db.update(sql)

    def load(self, id):
        sql = "select * from %s where id=%s" % (self.tableName, id)
        rows = self.query(sql)
        if rows == None or len(rows) == 0:
            return None
        row = rows[0]
        return row

    def delete(self, id):
        sql = "delete from %s where id=%s" % (self.tableName, id)
        return self.update(sql)

    def rows(self):
        sql = "select * from %s" % self.tableName
        items = self.query(sql)
        if items == None or len(items) == 0:
            return []
        return items

    def isColumnExists(self, where):
        sql = "select count(*) as cnt from %s %s" % (self.tableName, where)
        rows = self.query(sql)
        if rows == None or len(rows) == 0:
            return False
        row = rows[0]
        cnt = row['cnt']
        if cnt <= 0:
            return False
        else:
            return True

    def lastrowid(self):
        return mysql_db.lastrowid()

    def getVariMapByVariList(self, l):
        '''
        将列表中的多个变量组成一个字典
        '''
        m = {}
        for item in l:
            key = item['key']
            value = item['value']
            m[key] = value
        return m

    def jd(self, string, jdaLength=10):
        length = len(string)
        if length <= jdaLength:
            return string
        jd_str = string[0:jdaLength]
        return jd_str + '...'