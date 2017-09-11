#-*-coding:utf8-*-
import re
import bcrypt
from sqlalchemy import or_
from .Encrypt import encrypt, decrypt
from application.models.Database import Profile, User, DnsRecords, db


def getuid(username):
    userid = db.query(User.userid).filter_by(username=username).first()
    return userid

def checkpassword(username, password):
    user = Profile.query.filter_by(identifier=username).first()
    realpassword = ''.join(user.credential).encode('utf-8')
    password = decrypt(password)
    return True if bcrypt.hashpw(password, realpassword) else False

def checkuser(username):
    username = username.strip()
    user = User.query.filter_by(username=username).first()
    return True if user else False

def checkemail(userid, email):
    email = email.strip()
    chkemail = Profile.query.filter(Profile.userid != userid). \
               filter_by(identify_type='email', identifier=email).all()
    return True if chkemail else False


def checkphone(userid, phone):
    phone = phone.strip()
    chkemail = Profile.query.filter(Profile.userid != userid). \
              filter_by(identify_type='phone', identifier=phone).all()
    return True if chkmail else False

def checkdomain(domain):
    domain = domain.strip()
    chkdomain = DnsRecords.query.filter(or_(DnsRecords.host==domain,  \
                DnsRecords.zone==domain)).first()
    return True if chkdomain else False

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

