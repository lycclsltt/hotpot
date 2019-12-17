from controller.index import Index
from controller.user import Login
from controller.user import DemoLoginCommit
from controller.user import Logout
from controller.example import Hello

routers = {
    '/hello':Hello,
    '/': Index,
    '/user/login': Login,
    '/user/login_commit': DemoLoginCommit,
    '/user/logout': Logout,
}
