from sanic import Sanic
from decouple import config
import router.router as router
from sanic_session import Session, InMemorySessionInterface


class AppFactory:
    @classmethod
    def createApp(cls, appName):
        app = Sanic(appName)
        #判断session
        if config('SESSION_ENABLE') == 'true':
            # 启用session
            Session(app,
                    interface=InMemorySessionInterface(
                        expiry=int(config('SESSION_EXPIRE'))))
        #加载路由
        for uri, action in router.routers.items():
            app.add_route(action.as_view(), uri)
        #设置静态目录
        app.static('/static', './static')

        return app
