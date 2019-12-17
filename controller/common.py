from sanic.response import text, html
from sanic.views import HTTPMethodView
import demjson
from jinja2 import Environment, FileSystemLoader
from sanic import response
from decouple import config


class Common(HTTPMethodView):

    env = Environment(loader=FileSystemLoader('static/html/'))

    def __init__(self):
        self.request = None
        self.data = {}

    def get(self, request):
        return self.dispatchRequest(request)

    def post(self, request):
        return self.dispatchRequest(request)

    def genResponse(self, resp):
        if type(resp) == str:
            return text(resp)
        else:
            return resp

    def dispatchRequest(self, request):
        self.request = request
        ret = self.beforeHandle()
        if ret != None: return self.genResponse(ret)
        ret = self.handle()
        return self.genResponse(ret)

    def beforeHandle(self):
        return None

    def handle(self):
        return ''

    def req(self, k):
        v = ''

        #post里如果存在，优先返回post中的
        try:
            paramList = self.request.form[k]
            v = ','.join(paramList)
            return v
        except:
            pass

        #post中如果不存在，继续从get参数中查找
        try:
            paramList = self.request.args[k]
            v = ','.join(paramList)
            return v
        except:
            pass

        return v.strip()

    def resp(self, errno=0, errmsg='', data=''):
        ret = {'errno': errno, 'errmsg': str(errmsg), 'data': data}
        return demjson.encode(ret)

    def render(self, tpl):
        template = Common.env.get_template(tpl)
        content = template.render(data=self.data)
        return html(content)

    def session(self, k, v=None):
        if v == None:
            # get
            try:
                v = self.request['session'].get(k)
            except:
                pass
            if v == None: v = ''
        else:
            # set
            self.request['session'][k] = v
        return v

    def redirect(self, url):
        return response.redirect(url)

    def sessionKill(self):
        # 清理session
        self.request['session'].clear()

    def jd(self, string, jdaLength=6):
        length = len(string)
        if length <= jdaLength:
            return string
        jd_str = string[0:jdaLength]
        return jd_str + '...'


class NoAuth(Common):
    pass


class Auth(Common):

    OPER_ADD = 'add'
    OPER_EDIT = 'edit'

    def __init__(self):
        Common.__init__(self)
        self.data['session'] = {}

    def beforeHandle(self):
        if self.auth() == False:
            return self.redirect('/user/login')

    def auth(self):
        domain_name = self.session('domain_name')
        role = self.session('role')
        if domain_name == '' or domain_name == None:
            return False
        self.data['session']['domain_name'] = domain_name
        self.data['session']['role'] = role
        return True


class Admin(Auth):
    def __init__(self):
        Auth.__init__(self)

    def beforeHandle(self):
        if self.auth() == False:
            return self.redirect('/user/login')
        if self.session('role') != 'admin':
            return 'No permission, please contact admin'


class Guest(Auth):
    def __init__(self):
        Auth.__init__(self)


class Api(NoAuth):
    def beforeHandle(self):
        token = self.req('token')
        if token != config('API_TOKEN'):
            return self.resp(errno=1, errmsg='token is invalid')
        else:
            return None
