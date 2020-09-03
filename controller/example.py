from controller.common import NoAuth
from model.example import ExampleModel


class OrmSelect(NoAuth):
    def handle(self):
        exampleModel = ExampleModel()
        rows = exampleModel.rows()
        return self.resp(data=rows)


class Hello(NoAuth):
    def handle(self):
        return 'Hello hotpot!'


class GetParam(NoAuth):
    def handle(self):
        name = self.req('name')
        return 'Hello ' + name


class Page(NoAuth):
    def handle(self):
        name = self.req('name')
        self.data['name'] = name
        return self.render('page.html')


from decouple import config


class ReadConfig(NoAuth):
    def handle(self):
        token = config('API_TOKEN')
        return 'token is:' + token


class Status(NoAuth):
    def handle(self):
        return 'ok'
