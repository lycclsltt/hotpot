from controller.common import Guest


class Index(Guest):
    def handle(self):
        return self.render('index2.html')
