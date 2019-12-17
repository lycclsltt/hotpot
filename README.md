## 1.hotpot是什么？

###### hotpot是一个集成了前后端组件和实用工具类库的高性能python框架。使用hotpot可以快速进行业务开发，例如编写网站或API。帮助你快速完成开发任务，彻底告别996!



## 2.环境要求
###### python3.6+

## 3.快速开始

##### 环境准备
```shell script
1.获取源码: git clone 或从git 下载
2.安装依赖: pip3 install -r ./requirements.txt
3.执行./dev_restart.sh
4.访问 http://127.0.0.1:10001/hello 
```
 

##### 快速开发一个API
###### 1.在controller里创建一个类，继承NoAuth类，重写handle()方法（可参考controller/example.py）
```python
from controller.common import NoAuth


class Hello(NoAuth):
    def handle(self):
        return 'Hello hotpot!'
```

###### 2.添加路由 (可参考router/router.py)
```python
from controller.example import Hello, GetParam

routers = {
    '/hello': Hello,
}
```
###### 3.执行执行./dev_restart.sh，访问 http://127.0.0.1:10001/hello

##### 获取GET/POST请求参数, 通过req()方法，若参数不存在返回空字符串
```python
class GetParam(NoAuth):
    def handle(self):
        name = self.req('name')
        return 'Hello ' + name
```