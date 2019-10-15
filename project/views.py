from main import app
from flask import render_template,redirect,jsonify
from flask import request
from get_date import MyDate
import hashlib,os
from models import *
from settings import STATIC_PATH
import functools
from flask import session
import datetime

@app.route('/base/')
def base():
    return render_template('base.html')



### 登录装饰器
def loginValid(func):
    @functools.wraps(func) ### 保留原来的函数名字
    def inner(*args,**kwargs):
        cookie_email = request.cookies.get('email')
        user_id = request.cookies.get('user_id')
        session_email = session.get('email')
        if cookie_email and user_id and session_email:
            user = User.query.filter(User.email==cookie_email,User.id==user_id).first
            if user:
                return func(*args,**kwargs)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    return inner

## 登录
@app.route('/login/',methods=['post','get'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = User.query.filter(User.email==email).first()
            if user:
                if setPassword(password) == user.password:
                    # return redirect('/index/')
                    response = redirect('/index/')
                    response.set_cookie('email',email)
                    response.set_cookie('user_id',str(user.id))
                    session['email'] = email
                    return response
                else:
                    err_msg = '密码不正确'
            else:
                err_msg = '用户不存在，去注册'
        else:
            err_msg = '用户名和密码不能为空'
    return render_template('login.html',**locals())


###密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


## 注册
@app.route('/register/',methods=['post','get'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        if email and username:
            user = User.query.filter(User.email == email).all()
            if not user:
                if password == password2:
                    user = User(name=username,email=email,password=setPassword(password))
                    user.save()
                    return redirect('/login/')
                else:
                    err_msg = '两次密码不一致'
            else:
                err_msg = '该用户已存在，去登录'
        else:
            err_msg = '密码和用户名不能为空'

    return render_template('register.html',**locals())

@app.route('/forgot/password/',methods=['post','get'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user = User.query.filter(User.email==email).first()
            if user:
                return redirect('/reset/password/')
            else:
                err_msg = '用户不存在'
        else:
            err_msg = '邮箱不能为空'
    return render_template('forgot-password.html',**locals())

@app.route('/reset/password/',methods=['get','post'])
def resetPassword():
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        if password and password2 and email:
            user = User.query.filter(User.email == email).first()
            if user:
                user.password = setPassword(password)
                user.merge()
                err_msg = '重置成功'
            else:
                err_msg = '邮箱错误'
        else:
            err_msg = '邮箱或密码不能为空'



    return render_template('reset_password.html',**locals())

# 登出
@app.route('/logout/')
def logout():
    response = redirect('/login/')
    response.delete_cookie('email')
    response.delete_cookie('user_id')
    del session['email']
    return response


## 首页
@app.route('/index/')
@loginValid
def index():
    return render_template('index.html')


## 个人信息详情页
@app.route('/userinfo/')
@loginValid
def userinfo():
    result = MyDate().print_result()
    ### 通过cookie传过来的id获取对象
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    return render_template('userinfo.html',**locals())


## 完善个人信息页
@app.route('/update/userinfo/',methods=['post','get'])
@loginValid
def updateinfo():
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        if username:
            user.name = username
        if data.get('email'):
            user.email = data.get('email')
        if data.get('identity'):
            user.identity = data.get('identity')
        if data.get('age'):
            user .age = data.get('age')
        if data.get('term'):
            user.term = data.get('term')
        if data.get('phone'):
            user.phone = data.get('phone')
        if data.get('sex'):
            user.sex = data.get('sex')
        ### 保存图片
        if request.files.get('photo'):
            ## 图片名称
            photo = request.files.get('photo')
            filename = request.files.get('photo').filename
            photo_path = os.path.join('images',filename)
            path = os.path.join(STATIC_PATH,photo_path)
            photo.save(path)   ## 将文件保存在path下
            user.photo = photo_path

        user.merge()

    return render_template('update_info.html',**locals())


## 请假条
@app.route('/leave_list/',methods=['post','get'])
@loginValid
def leave_list():
    if request.method == 'POST':
        user_id = request.cookies.get('user_id')
        data = request.form
        if len(data) == 7:
            leave = Leave()
            leave.leave_id = int(user_id)
            leave.leave_name = data.get('username')
            leave.leave_type = data.get('type')
            if data.get('starttime'):
                leave.leave_start = datetime.datetime.strptime(data.get('starttime'),'%Y-%m-%d')
            if data.get('endtime'):
                leave.leave_end = datetime.datetime.strptime(data.get('endtime'),'%Y-%m-%d')
            leave.leave_description = data.get('description')
            leave.leave_phone = data.get('phone')
            leave.leave_status = 0
            leave.leave_days = data.get('days')
            leave.save()
        return redirect('/leave_all_list/')
    return render_template('leave_list.html')


## 当前登录用户的所有请假条
@app.route('/leave_all_list/')
def leave_all_list():
    user_id = request.cookies.get('user_id')
    leave = Leave.query.filter(Leave.leave_id == user_id).all()
    return render_template('leave_all_list.html',**locals())

## 当前登录用户的某个请假条的详情
@app.route('/leave_detail/')
@loginValid
def leave_detail():
    user_id = request.cookies.get('user_id')
    id = request.args.get('id')  ## leave表的id,请假条的id
    leave = Leave.query.filter(Leave.leave_id == user_id,Leave.id == id).first()
    # print(leave)
    return render_template('leave_detail.html',**locals())


## 实现审核请假条的功能
@app.route('/check_leave/')
@loginValid
def check_leave():
    result = {
        'code':1000,
        'content':''
    }
    user_id = request.cookies.get('user_id') ## 当前登陆用户的id
    leave_type = request.args.get('result')
    leave_id = request.args.get('leave_id')  ## leave表的id
    leave = Leave.query.filter(Leave.leave_id == user_id, Leave.id == leave_id).first()
    if leave:
        if leave_type == '通过':
            leave.leave_status = 1
            leave.merge()
        elif leave_type == '销假':
            leave.leave_status = 3
            leave.merge()
        elif leave_type == '驳回':
            leave.leave_status = 2
            leave.merge()

    else:
        result['code'] = 10001
        result['content'] = '假条不存在'

    return result
