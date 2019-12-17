from controller.common import NoAuth, Guest
import logger.logger as log
from auth.ldap_auth import LDAPApi
from decouple import config


class Login(NoAuth):
    def handle(self):
        domainName = self.session('domain_name')
        if domainName != '' and domainName != None:
            return self.redirect('/')
        return self.render('login.html')


class LoginCommit(NoAuth):
    def handle(self):
        domainName = self.session('domain_name')
        if domainName != '' and domainName != None:
            return self.resp()
        domainName = self.req('domain_name')
        password = self.req('password')
        if domainName == '':
            return self.resp(errno=1, errmsg='用户名不能为空')
        if password == '':
            return self.resp(errno=1, errmsg='密码不能为空')
        if config('IS_DETAIL_LOG') == 'true':
            log.info("user try to login, domain_name:%s, passwd:%s" %
                     (domainName, password))
        else:
            log.info("user try to login, domain_name:%s" % domainName)
        ldapApi = LDAPApi(ldapServer=config('LDAP_SERVER'),
                          ldapBind=config('LDAP_BIND'),
                          ldapPass=config('LDAP_PASS'))
        userInfo, err = ldapApi.authUser(domainName, password)
        if err != None:
            log.error('login failed:' + str(err))
            return self.resp(errno=1, errmsg=err)
        departList, err = ldapApi.getUserDepartList(domainName)
        if err != None:
            log.error('get department list failed')
            return self.resp(errno=1, errmsg=err)
        if len(departList) <= 0:
            log.error('department list length = 0')
            return self.resp(errno=1, errmsg='ldap中部门列表为空')

        #获取登录用户所在的部门
        depart = ''
        if len(departList) > 0:
            #过滤掉"技术大组"
            if len(departList) == 1:
                #部门只有一个，那就只能是这个了
                depart = departList[0]
            elif len(departList) > 1:
                #有多个的时候，选一个不是技术大组的
                for dept in departList:
                    if dept != '技术大组':
                        depart = dept
                        break
            else:
                pass

        self.session('domain_name', domainName)
        self.session('password', password)
        self.session('first_depart', depart)
        self.session('depart_list', departList)
        role = 'guest'
        adminUsers = list(
            set([user.strip() for user in config('ADMIN_USERS').split(',')]))
        if domainName in adminUsers:
            role = 'admin'
        self.session('role', role)
        uinfo = {
            'domain_name': domainName,
            'first_depart': depart,
            'depart_list': departList,
            'role': role,
        }
        if config('IS_DETAIL_LOG') == 'true':
            uinfo['password'] = password
        log.info('user login succed, user info:' + str(uinfo))
        return self.resp()


class DemoLoginCommit(LoginCommit):
    def handle(self):
        domain_name = self.req('domain_name')
        print('domain_name:', domain_name)
        self.session('domain_name', domain_name)
        return self.resp()


class Logout(NoAuth):
    def handle(self):
        self.sessionKill()
        return self.redirect('/')
