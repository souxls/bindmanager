#-*- coding:utf8 -*-
import json
from datetime import datetime
from urlparse import urlparse, urljoin
from flask import ( request, Response, Blueprint, render_template,
    url_for, redirect)
from flask_login import login_required, login_user, logout_user
from application import login_manager
from application.models.Database import Profile, User, db
from application.models.Encrypt import encrypt, decrypt
from application.models.utils import checkuser, checkpassword

auth = Blueprint('auth', __name__,
                    template_folder='templates/login',
                    static_folder='static')


@login_manager.user_loader
def user_loader(username):
    return User.query.filter(User.username==username).first()

#@login_manager.request_loader
#def request_loader(request):
#    username = request.get('email')
#    if email not in users:
#        return

#    user = User()
#    user.id = email
#    user.is_authenticated = request.form['pw'] == users[email]['pw']
#    return user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/index.html')
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        loginip = request.headers.get('X-Real-IP', request.remote_addr)
        nowtime = datetime.now()
        if checkuser(username):
            if checkpassword(username, password):
                updateuser = User.query.filter(username==username).first()
                updateuser.last_login_ip = loginip
                updateuser.last_login_date = nowtime
                db.session.add(updateuser)
                db.session.commit()
                curr_user = User()
                curr_user.id = username
                login_user(curr_user) 
                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)
                successurl = next or url_for('dashboard.index')
                data = {"status": "success", "url": successurl, "message": "登录成功"}
            else:
                data = {"status": "fail", "error": "用户密码错误"}
        else:
             data = {"status": "fail", "error": "用户名错误"} 
        return Response(json.dumps(data),  content_type='application/json',
                       mimetype='application/json')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
