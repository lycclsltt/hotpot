

- [hotpot是什么？](#hotpot是什么)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
  - [快速开发一个API](#快速开发一个api)
  - [获取GET/POST请求参数](#获取getpost请求参数)
  - [返回json格式的接口数据](#返回json格式的接口数据)
  - [服务端渲染 (与jinja2模版引擎语法一致)](#服务端渲染-与jinja2模版引擎语法一致)
  - [配置文件说明](#配置文件说明)
  - [读取配置文件](#读取配置文件)
  - [ORM使用 (可参考model/example.py)](#orm使用-可参考modelexamplepy)
  - [目录结构说明](#目录结构说明)

## hotpot是什么？

hotpot是一个简单、易用的python框架。基于高性能sanic, 集成了Session/ORM/日志处理/LDAP 以及常用工具类库。使用hotpot可以快速进行业务开发，例如编写网站或API。相比django更简单，轻松上手。相比flask, web.py 等框架，更具有规范性，更适合大型工程，同时性能更好。
   
hotpot设计的初衷是：python代码拥有很高的开发效率，但由于开发者能力不同，易造成开发速度快，后期维护成本高的问题。hotpot希望通过框架的约定规则和限制规避此类问题，增强python程序的可维护性。


## 环境要求
python3.6+

## 快速开始

环境准备
```shell script
1.获取源码: git clone 或从git 下载
2.安装依赖: pip3 install -r ./requirements.txt
3.执行./dev_restart.sh
4.访问 http://127.0.0.1:10001/hello 
```


##### 快速开发一个API
1.在controller里创建一个类，继承NoAuth类，重写handle()方法（可参考controller/example.py）
```python
from controller.common import NoAuth


class Hello(NoAuth):
    def handle(self):
        return 'Hello hotpot!'
```

2.添加路由 (可参考router/router.py)
```python
from controller.example import Hello

routers = {
    '/hello': Hello,
}
```
3.执行执行./dev_restart.sh，访问 http://127.0.0.1:10001/hello

##### 获取GET/POST请求参数
```python
class GetParam(NoAuth):
    def handle(self):
        name = self.req('name')  #req()方法可以获取GET/POST请求中的参数，若参数不存在返回空字符串
        return 'Hello ' + name
```

##### 返回json格式的接口数据
```python
class GetParam(NoAuth):
    def handle(self):
        name = self.req('name')
        if name == '':
            return self.resp(errno=1, errmsg = 'name参数必填')
        else:
            return self.resp(data = 'Hello ' + name)
```
##### 服务端渲染 (与jinja2模版引擎语法一致)
1.在static/html中添加一个page.html
```html
<h1>Hello {{data.name}}</h1>
```
2.添加路由，参考上面的方法
3.在controller里添加类
```python
class Page(NoAuth):
    def handle(self):
        name = self.req('name')   #获取请求参数
        self.data['name'] = name  #赋值到data属性中，data属性用来渲染页面
        return self.render('page.html')  #渲染static/html/page.html 页面
```
4.执行执行./dev_restart.sh，访问 http://127.0.0.1:10001/page?name=小明

##### 配置文件说明
配置文件有两个，用于将测试环境、生产环境区分开, 分别是:  
settings.ini.dev：测试环境配置文件，通过dev_restart.sh启动服务后，读取该文件作为配置文件。  
settings.ini.prod：生产环境配置文件，通过prod_restart.sh启动服务后，读取该文件作为配置文件。  

目前支持的配置项有：
```ini
[settings]

#版本号，服务启动后会将版本号写入到日志文件中，便于排查问题
VERSION = 0.0.1

#请求日志, true开启，false关闭
ACCESS_LOG = false

#用于调试，true开启，false关闭，开启后会在终端显示更多运行时信息
DEBUG = true

#是否同时输出日志到终端，true开启，false关闭，若开启，日志不但会写入到日志文件，还会输出到终端，推荐在测试环境使用
LOG_OUTPUT = false

#监听端口
PORT = 10001

#工作线程数
WORKER_NUM = 1

#日志文件
LOG_FILE = ./logs/app.log

#是否启用session，true启用, false关闭
SESSION_ENABLE = true

#session过期时间，单位：秒
SESSION_EXPIRE = 36000

#数据库配置
#地址
DB_HOST = 127.0.0.1
#端口
DB_PORT = 3306
#用户名
DB_USER = xdev
#密码 
DB_PWD = xdev
#数据库名称
DB_NAME = test_db
#连接池最小连接数
DB_POOL_MIN_CONNECTION = 10
#连接超时
DB_POOL_CONNECT_TIMEOUT = 10
#读取超时
DB_POOL_READ_TIMEOUT = 10

###ldap登录验证
LDAP_SERVER = ldap://10.10.36.28:389
LDAP_BIND = CN=readonly,CN=Users,DC=xxx,DC=com
LDAP_PASS = xxxx

#请求API时用于验证的token
API_TOKEN = hotpot_api_token
```

##### 读取配置文件
除了上述框架使用的配置之外，你还可以在settings.ini.dev或settings.ini.prod中添加自定义配置，并从代码中读取。例如：   
首先在settings.ini.dev中添加配置（如果是生产环境，添加到settings.ini.prod中）
```ini
API_TOKEN = hotpot_api_token
```
然后在controller中读取，例如：
```python
from decouple import config
class ReadConfig(NoAuth):
    def handle(self):
        token = config('API_TOKEN')
        return 'token is:' + token
```
访问 http://127.0.0.1:10001/read_config

##### ORM使用 (可参考model/example.py)
1.在model中创建一个类，继承CommonModel类
```python
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
            'test_name': name,
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
```
2.在controller中调用
```python
from controller.common import NoAuth
from model.example import ExampleModel

class OrmSelect(NoAuth):
    def handle(self):
        exampleModel = ExampleModel()
        rows = exampleModel.rows()
        return self.resp(data=rows)
```
##### 目录结构说明
hotpot从开发者的角度出发，设想构建一个项目所需要的所有目录，无论你是添加脚本，定时任务，切割日志的配置文件，nginx配置文件还是业务代码，都可以按照下面目录的用途进行存放。这样做的目的是确保和项目相关的所有文件可以被保存起来，有利于项目的维护。
```
├── CHANGELOG.md    #表更记录, 都懂的
├── README.md       #README.md， 都懂的 
├── agileutil       #工具包
├── app_init.py     #web服务启动前执行里面的app_init()方法 
├── auth            #ldap验证相关工具
├── controller      #控制器 (mvc中的c)
├── db              #声明使用的数据库
├── dev_restart.sh  #测试环境启动脚本
├── engine          #框架相关代码
├── hotpot.py       #框架启动的入口文件
├── logger          #日志库
├── logrotate       #用于存放需要切割的日志
├── logs            #用于存放服务日志
├── model           #模型层 (mvc中的m)
├── nginx_conf      #用于存放nginx配置文件
├── prod_restart.sh #生产环境启动脚本
├── requirements.txt# #服务的所有依赖
├── router            #用于添加路由
├── script            #用于添加一些脚本
├── settings.ini -> ./settings.ini.dev 
├── settings.ini.dev  #测试环境配置文件
├── settings.ini.prod #生产环境配置文件
├── sql               #用于存放建标语句等
├── static            #用于存放静态文件(html, js, css)
└── task              #用于添加定时任务
```