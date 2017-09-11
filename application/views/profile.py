#-*-coding:utf8-*-
import json
from flask import (Blueprint, render_template, request, Response,
    url_for, redirect )
from flask_login import login_required, current_user
from application.models.Database import ( getusersinfo, adduser,
    deluser, User, Profile, db, chagepwd )
from application.models.utils import ( checkuser, checkemail,
    checkphone, checkpassword, getuid )
from application.models.Encrypt import encrypt

profile = Blueprint('profile', __name__,
                    template_folder='templates/profile',
                    static_folder='static')

@profile.route('/user', methods=["GET","POST"])
@login_required
def user():
    username = current_user.username    
    password = db.session.query(Profile.identifier).filter(Profile.identity_type=='username'). \
                   filter(Profile.userid==current_user.id).first()
    curr = db.session.query(Profile.identifier).filter(Profile.identity_type=='email'). \
                filter(Profile.userid==current_user.id).first()
    email = curr._asdict()["identifier"] if curr else None

    curr = db.session.query(Profile.identifier).filter(Profile.identity_type=='phone'). \
                filter(Profile.userid==current_user.id).first()
    phone = curr._asdict()["identifier"] if curr else None

    if request.method == 'POST':
        postdata = request.form
        if checkuser(username):
            if 'nickname' in postdata:
                nickname = postdata['nickname']
                email = postdata['email']
                phone = postdata['phone']
                user = User.query.filter_by(username=username).first()
                user.nickname = nickname
                db.session.commit()
                userid = current_user.id
                if checkmail(userid, email):
                    profile = Profile.query.filter_by(userid=userid, identity_type='email').first()
                    profile.identity_type = 'email'
                    profile.identifier = email
                    password = profile.credential
                    db.session.commit()
                else:
                    data = {"status": "fail", "error": "邮箱已被注册"}
                profile = Profile.query.filter_by(userid=userid, identity_type='phone').first()
                if checkphone(userid, phone):
                    if profile:
                        profile.identity_type = 'phone'
                        profile.identitifer = phone
                        db.session.commit()
                    else:
                        profile = Profile()
                        profile.userid =userid
                        profile.identity_type = 'phone'
                        profile.identifier = postdata['phone']
                        profile.credential = password
                        db.session.add(profile)
                        db.session.commit()
                    data = {"status": "success", "message": "用户信息更新成功"}
            else:
                data = {"status": "fail", "error": "请求错误"}
            return Response(json.dumps(data), content_type='application/json',
                            mimetype='application/json')
    return render_template('profile/user.html', current_user=current_user, 
                           curr_email=email, curr_phone=phone)

@profile.route('/manager', methods=["GET", "POST"])
@login_required
def manager():
    if current_user.auth != 1:
        return redirect(404)
    users = getusersinfo()
    return render_template("profile/manager.html", users=users)
    
@profile.route('/manager/add', methods=["GET", "POST"])
@login_required
def add():
    if current_user.auth != 1:
        return redirect(404)

    if request.method == 'POST':
        postdata = request.form
        username = postdata['username']
        nickname = postdata['nickname']
        password = postdata['password']
        email = postdata['email']
        auth = postdata['auth']
        loginip = request.headers.get("X-Real-IP", request.remote_addr)
        userid = getuid(username)
        if not checkuser(username) and checkemail(userid, email):
            password = encrypt(password) if password else None
            adduser(username, nickname, password, email, loginip, auth)
            successurl = url_for('profile.manager')
            data = {"status": "success", "url": successurl, "message": "用户添加成功"} 
        else:
            data = {"status":"fail", "error": "用户名或邮箱已被占用"}
        return Response(json.dumps(data),  content_type='application/json',
                       mimetype='application/json')

    return render_template("profile/add.html", current_user=current_user)

@profile.route('/manager/delete', methods=["POST"])
@login_required
def delete():
    postdata = request.get_json()
    username = postdata['username']
    username = username.strip()
    if checkuser(username):
        deluser(username)
        data = {"status":"success", "message": "用户删除成功"}
    else:
        data = {"status": "fail", "error": "用户不存在"}
    return Response(json.dumps(data), content_type='application/json',
                    mimetype='application/json')

@profile.route('/user/changepassword', methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == 'POST':
        postdata = request.form
        if checkuser(username):
            oldpassword = postdata['password']
            if checkpassword(username, oldpassword):
                password = postdata['newpassword']
                password = password.strip()
                password = encrypt(password)
                chagepwd(username,oldpassword, password)
                successurl = url_for('/user')
                data = {"status":"success", "url": successurl, "message": "密码修改成功"}
            else:
                data = {"status":"fail", "error": "原密码输入错误，请重新输入"}
        else:
            data = {"status":"fail", "error": "请求出错"}
        return Response(json.dumps(data), content_type='application/json',
                        mimetype='application/json')
    return render_template('profile/changepassword.html', current_user=current_user)
