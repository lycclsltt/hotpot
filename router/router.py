from controller.index import Index
from controller.user import Login
from controller.user import DemoLoginCommit
from controller.user import Logout

routers = {
    '/': Index,
    '/user/login': Login,
    '/user/login_commit': DemoLoginCommit,
    '/user/logout': Logout,
}
