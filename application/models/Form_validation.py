#-*-coding:utf8-*-
from flask import request


def form_validation(data)
    for k,v in data:
        if k == 'username':
        username = postdata['username']
        nickname = postdata['nickname']
        password = postdata['password']
        email = postdata['email']
        auth = postdata['auth']

def checkdata(datatype, data):
    chkdata = data.strip()
    regdomain = re.compile(u'^[\w\d]+\.[\w\d]+$', re.M)
    regip = re.compile(u'^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$', re.M)
    regnum = re.compile(u'^\d+$', re.M)
    reghost = re.compile(u'^[.\d\w_-]+$', re.M)
    if datatype == 'domain' and re.match(regdomain, chkdata):
        return chkdata
    elif datatype == 'ip' and re.match(regip, chkdata):
        return  chkdata
    elif datatype == 'num' and re.match(regnum, chkdata):
        return chkdata
    elif datatype == 'host' and re.match(reghost, chkdata):
        return chkdata
    else:
        return False
