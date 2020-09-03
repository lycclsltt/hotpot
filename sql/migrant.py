#coding=utf-8

'''
Usgae:
cd sql
python3 migrant.py
'''

import os
from decouple import config
from agileutil.db4 import PoolDB
import subprocess
cmd = "mysql -h'%s' -P'%s' -u'%s' -p'%s' " % (
    config('DB_HOST'),
    config('DB_PORT'),
    config('DB_USER'),
    config('DB_PWD')
)
files = os.listdir('./')
for filename in files:
    if '.sql' in filename:
        tmpCmd = cmd + " -e 'source ./%s'" % filename
        status, output = subprocess.getstatusoutput(tmpCmd)
        if status == 0:
            print('[INFO] %s ok' % filename)
        else:
            print('[ERROR] %s failed:%s' % (filename, output) )