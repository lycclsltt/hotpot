from model.common import CommonModel
from agileutil.db4 import Orm
import db.mysql as dbInstance


class ExampleModel(CommonModel):
    def __init__(self):
        #表名字
        self.tableName = 'test_tb'

    def add(self, name):
        '''
        insert示例
        '''
        return Orm(dbInstance).table(self.tableName).data({
            'test_name': name,
        }).insert()

    def deleteByName(self, name):
        '''
        delete示例
        '''
        return Orm(dbInstance).table(self.tableName).where(
            'test_name', '=', name).delete()

    def updateRow(self, name, id):
        '''
        update示例
        '''
        return Orm(dbInstance).table(self.tableName).where('id', id).data({
            'test_name':
            name,
        }).update()

    def rows(self):
        '''
        select示例
        '''
        rows = Orm(dbInstance).table(self.tableName).get()
        return rows

    def getByName(self, name):
        '''
        select示例
        '''
        row = Orm(dbInstance).table(self.tableName).where(
            'test_name', '=', name).first()
        return row
