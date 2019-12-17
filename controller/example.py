from controller.common import NoAuth


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
