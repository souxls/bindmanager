#-*-coding:utf8-*-
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, not_
from flask_login import UserMixin
from application import app


db = SQLAlchemy(app)

tables = ['DnsRecords']


class User(UserMixin, db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True)
    nickname = db.Column(db.String(255))
    auth = db.Column(db.Integer)
    last_login_ip = db.Column(db.String(64))
    last_login_date = db.Column(db.DateTime(), default=datetime.now())
    create_date = db.Column(db.DateTime())
    status = db.Column(db.Integer)

class Profile(db.Model):
  
    __tablname__ = 'profile'

    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    identity_type = db.Column(db.String(255))
    identifier = db.Column(db.String(255))
    credential = db.Column(db.String(255))


class DnsRecords(db.Model):

    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.VARCHAR(255))
    ttl = db.Column(db.Integer, default=86400)
    type = db.Column(db.VARCHAR(255))
    linetype = db.Column(db.VARCHAR(255))
    host = db.Column(db.VARCHAR(255))
    mx_priority = db.Column(db.Integer)
    data = db.Column(db.Text)
    primary_ns = db.Column(db.VARCHAR(255))
    resp_contact = db.Column(db.VARCHAR(255))
    serial = db.column(db.Integer)
    refresh = db.Column(db.Integer)
    retry = db.Column(db.Integer)
    expire = db.Column(db.Integer)
    minimum = db.Column(db.Integer)
    status = db.Column(db.Integer, default=1)

def addrecords(zone, host, type, data, ttl, linetype, status):
    records = DnsRecords()
    records.zone = zone
    records.ttl = ttl
    records.data = data
    records.type = type
    records.host = host
    records.linetype = linetype
    records.status = status
    try:
        db.session.add(records)
        db.session.commit()
    except Exception,e:
        return False
    return True

def adddomain(domain):
    records = DnsRecords()
    records.zone = domain
    records.type = 'SOA'
    records.host = '@'
    records.primary_ns = 'ns1.wanmeilink.com.'
    records.serial = datetime.strftime(datetime.now(), "%Y%M%d%H")
    records.refresh = 300
    records.retry = 300
    records.expire = 432000
    records.minimum = 14400
    db.session.add(records)
    db.session.commit()
    nslist = ["ns1.wanmeilink.com", "ns2.wanmeilink.com", "ns3.wanmeilink.com", "ns4.wanmeilink.com"]
    for i in nslist:
        records = DnsRecords()
        records.zone = domain
        records.type = 'NS'
        records.host = '@'
        records.data = i
        db.session.add(records)
        db.session.commit()
        data = {"status": "fail", "error": "NS add failed" }
    

def delrecords(domain, host, data, type, linetype):
    delrecords = DnsRecords.query.filter_by(host=host, zone=domain, type=type, linetype=linetype).first()
    try:
        db.session.delete(delrecords)
        db.session.commit()
    except Exception,e:
        return False
    return True

def searchrecords(zone, host):
    if not host:
        return DnsRecords.query.filter_by(zone=zone).filter(not_(DnsRecords.type=='SOA')). \
               order_by(DnsRecords.host.desc()).all()
    else:
        return DnsRecords.query.filter_by(host=host, zone=zone). \
               filter(not_(DnsRecords.type=='SOA')).order_by(DnsRecords.host.desc()).all()
    return DnsRecords.query.filter_by(zone=zone).filter(not_(DnsRecords.type=='SOA')). \
           order_by(DnsRecords.host.desc()).all()

def searchiprecords(ip):
    return DnsRecords.query.filter_by(data=ip).order_by(DnsRecords.host.desc()).all()
    

def getusersinfo(username=None):
    if username:
        users = db.session.query(User.username, User.nickname, User.status, \
                User.auth, Profile.identifier).join(Profile, User.id==Profile.userid). \
                filter(User.username==username).filter(Profile.identity_type=="username"). \
                order_by(User.id).first()
    else:
        users = db.session.query(User.username, User.nickname, User.status, \
                User.auth, Profile.identifier).join(Profile, User.id==Profile.userid). \
                filter(Profile.identity_type=='email').order_by(User.id).all()
    return users

def adduser(username, nickname, password, email, loginip, auth, status=1):
    now = datetime.now()
    user = User()
    user.username = username
    user.nickname = nickname
    user.last_login_ip = loginip
    user.last_login_date = now
    user.create_date = now
    user.status = status
    user.auth = auth
    try:
        db.session.add(user)
        db.session.commit()
    except Exception,e:
        return False
    user_id = db.session.query(User.id).filter(User.username==username).first()
    userid = user_id.id
    if userid:
        identity_username = Profile()
        identity_username.userid = userid
        identity_username.identity_type = "username"
        identity_username.identifier = username
        identity_username.credential = password
        try:
            db.session.add(identity_username)
            db.session.commit()
        except Exception, e:
            return False
        if email:
            identity_email = Profile()
            identity_email.userid = userid
            identity_email.identity_type = "email"
            identity_email.identifier = email
            identity_email.credential = password
            try:
                db.session.add(identity_email)
                db.session.commit()
            except Exception, e:
                return False
    return True

def deluser(username):
    user = User()
    userprofile = Profile()
    userid = db.session.query(User.id).filter(User.username==username).first()
    userid = userid[0]
    userprofiledel = Profile.query.filter_by(userid=userid).all()
    userdel = User.query.filter_by(username=username).first()
    for i in userprofiledel:
        db.session.delete(i) 
    try:
        db.session.delete(userdel)
        db.session.commit()
    except Exception,e:
        return False
    return True


def updateuser(username, userkey, uservalue):
    user = User()
    profile = Profile()
    user_id = db.session.query(User.id).filter(User.username==username).first()
    userid = user_id.id
    user.username = username
    if userkey == 'nickname':
        user.nickname = uservalue
    elif userkey == 'email':
        user.email = uservalue 
    elif userkey == 'phone':
        user.phone = uservalue
    elif userkey == 'status':
        user.status = uservalue
    elif userkey == 'auth':
        user.auth = uservalue
    elif userkey == 'email':
        profile.identity_type = 'email'
        profile.identitifer = uservalue
    elif userkey == 'phone':
        profile.identity_type = 'phone'
        profile.identitifer = uservalue
    else:
        return False
    try:
        db.session.add(user)
        db.session.commit()
    except Exception,e:
        return False
    return True

def chagepwd(username, password):
    userid = db.session.query(User.id).filter(User.username==username).first()
    profile = Profile()
    profile.userid = userid
    profile.credential = password
    try:
        db.session.add(profile)
        db.seesion.commit()
    except Exception,e:
        return False
    return True
