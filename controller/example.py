from controller.common import NoAuth

class Hello(NoAuth):
    def handle(self):
        return 'Hello hotpot!'