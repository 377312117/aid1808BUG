"""
Users中的视图以及路由函数
"""


import os
import random
from datetime import datetime
import json

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from . import users
from .. import db,login_required
from ..models import *

@users.route('/login',methods=['GET','POST'])
def login():
    '''用于登录'''
    if request.method == 'GET':
        if session.get('uname','') and session.get('upwd',''):
            print('session信息已存在,直接登录')
            return redirect('/')
        else:
            if request.cookies.get('uname','') and request.cookies.get('upwd',''):
                print('cookies中判断已经登录过,重定向至主页')
                return redirect('/')
            else:
                print('无cookie信息,请重新登录')
                return render_template('/login.html')
            print('无session信息,请重新登录')
            return render_template('/login.html')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        username = request.form.get('uname','')
        print('username:',username)
        upassword = request.form.get('upassword','')
        print('upassword:',upassword)

        user = db.session.query(Users).filter(Users.name == username).first()
        print('user:',user)
        if user and user.password==upassword:
            rememberme = request.values.get('rememberme','')
            print('rememberme:',rememberme)
            session['uname']=user.name
            session['upwd']=upassword
            session['uid'] = user.id

            print('*********************')
            print(session['uid'])
            print('*********************')
            if rememberme == "1":
                dic = {
                    'status':2,
                    'info':'已记住密码',
                }
            else:
                dic = {
                    'status':1,
                    'info':'未记住密码',
                }
            return json.dumps(dic)
        else:
            url=request.headers.get('Referer')
            dic = {
                'status':0,
                'url':url
            }
            return json.dumps(dic)



@users.route('/01-check',methods=['GET','POST'])
def check():
    '''检查用户名是否合格'''
    uname = request.args.get('uname','')
    print('uname:',uname)
    user= Users.query.filter_by(name=uname).first()
    if user:
        dic = {
            'status':1,
            'info':'该用户已经注册,可以登录',
        }
    else:
        dic = {
            'status':0,
            'info':'该用户未注册,不可登录',
        }
    return json.dumps(dic)

@users.route('/02-checknumber',methods=['GET','POST'])
def checknumber():
    '''检查手机号是否合格'''
    phonenumber = request.args.get('phonenumber','')
    print('phonenumber:',phonenumber)
    user= Users.query.filter_by(phonenumber=phonenumber).first()
    if user:
        dic = {
            'status':1,
            'info':'该手机号已经注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该手机号未注册,可继续注册',
        }
    return json.dumps(dic)

@users.route('/02-alternumber',methods=['GET','POST'])
def alternumber():
    '''检查手机号是否合格'''
    phonenumber = request.args.get('phonenumber','')
    uname= request.args.get('uname','')
    print('phonenumber:',phonenumber)
    print('uname',uname)
    user= Users.query.filter_by(phonenumber=phonenumber).first()
    yz_user = Users.query.filter_by(name=uname).first()
    if user and phonenumber != yz_user.phonenumber:
        dic = {
            'status':1,
            'info':'该手机号已经被其他用户注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该手机号未注册或您未修改您的号码,可继续注册',
        }
    return json.dumps(dic)

@users.route('/03-checkemail',methods=['GET','POST'])
def checkemail():
    '''检查邮箱是否合格'''
    uemail = request.args.get('uemail','')
    print('uemail:',uemail)
    user= Users.query.filter_by(email=uemail).first()
    if user:
        dic = {
            'status':1,
            'info':'该邮箱已经注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该邮箱未注册,可继续注册',
        }
    return json.dumps(dic)

@users.route('/03-alteremail',methods=['GET','POST'])
def alteremail():
    '''检查邮箱是否合格'''
    uemail = request.args.get('uemail','')
    print('uemail:',uemail)
    uname= request.args.get('uname','')
    print('uname',uname)
    user= Users.query.filter_by(email=uemail).first()
    yz_user = Users.query.filter_by(name=uname).first()
    if user and user != yz_user:
        dic = {
            'status':1,
            'info':'该邮箱已经注册,请重新输入',
        }
    else:
        dic = {
            'status':0,
            'info':'该邮箱未注册或您未修改邮箱,可继续修改',
        }
    return json.dumps(dic)

@users.route('/setsession',methods=['GET','POST'])
@login_required
def setsession():
    '''用于记住密码时设置session信息'''
    if  session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        upwd = session.get('upwd','')
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('********************')
        print(session['uid'])
        print('********************')
        resp = redirect('/')
        resp.set_cookie('uname',uname,7*24*60*60)
        resp.set_cookie('upwd',upwd,7*24*60*60)
        return resp

@users.route('/cancel',methods=['GET','POST'])
def cancel():
    '''用于注销信息'''
    resp = redirect('/')
    if 'uname' in session and 'upwd' in session:
        del session['uname']
        del session['upwd']
        del session['uid']
        if "district" in session:
            del session['district']
            del session['high_price']
            del session['low_price']
    if 'uname' in request.cookies and 'upwd' in request.cookies:
        resp.delete_cookie('uname')
        resp.delete_cookie('upwd')
    return resp

@users.route('/register',methods=['GET','POST'])
def register():
    '''用于注册'''
    if request.method == 'GET':
        return redirect('/')
    else:
        # 此用法用于查询该用户是否存在且密码是否正确
        try:
            username = request.form.get('uname','')
            upassword = request.form.get('upassword','')
            phonenumber = request.form.get('phonenumber','')
            uemail = request.form.get('uemail','')
            print(f'uname:{username},upassword:{upassword},phonenumber:{phonenumber},uemail:{uemail}')
            user = Users(name=username, email=uemail, phonenumber=phonenumber,password = upassword,selfinfo=None,imgpath=None)
            db.session.add(user)
            session['uname']=username
            session['upwd'] =upassword
            session['uid'] = user.id
            print('**************')
            print(session['uid'])
            print('***************')
            dic = {
                'status':1,
                'info':'恭喜你注册成功',
            }
        except Exception as e:
            print(e)
            dic = {
                'status':0,
                'info':'注册发生错误',
            }
        return json.dumps(dic)


@users.route('/private',methods=['GET','POST'])
# 用于拦截登录
@login_required
def private():
    '''用于展示个人主页'''
    uname=session.get('uname','')
    user = Users.query.filter_by(name=uname).first()
    # print('user:',user)
    if request.method == 'GET':
        # print(f"user:{user},{user.selfinfo}")

        histories = user.history_houses.distinct().all()[-1:-10:-1]

        collections = user.favor_houses.distinct().all()[::-1]

        if len(histories):
            message1 = "您的历史记录如下(只保留九条):"
        else:
            message1 = "您暂无历史记录，为您做如下推荐:"
            count = Houses.query.count()
            l = [random.randint(1, count) for _ in range(3)]
            histories = Houses.query.filter(Houses.id.in_(l)).all()

        if len(collections):
            message2 = "您的收藏记录如下:"
        else:
            message2 = "您暂未收藏任何房屋信息，为您做以下推荐:"
            count = Houses.query.count()
            print("******************************")
            print(count)
            print("******************************")
            l = [random.randint(1, count) for _ in range(9)]
            collections = Houses.query.filter(Houses.id.in_(l)).all()

        print("hellooooooooooooooooooooooo")

        return  render_template('/private.html',params=locals())
    else:
        if request.files.get('uimg',''):
            # 处理上传的文件
            # 1.得到上传的文件
            f = request.files.get('uimg')
            print('获取文件为:',f)
            # 2.将文件保存进指定的目录处
            # 3.或将文件保存进指定的目录处[绝对路径]
            # 获取当前文件所在的目录名
            # 加上上传时间格式化字符串作为文件名,避免重复datetime.now().strftime('%Y%m%d%H%M%S%f')
            # 获取文件扩展名
            ext = f.filename.split('.')[-1]
            filename =  datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + ext
            # 默认图片路径
            defaultpath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = defaultpath+r'/static/images/uploads/'+filename
            print('filepath:',filepath)


            f.save(filepath)


            user.imgpath = r'/static/images/uploads/'+filename


        if request.form.get('upassword','') :
            user.password = request.form.get('upassword','')
            session['upwd'] =request.form.get('upassword','')


        user.selfinfo = request.form.get('textarea','')
        user.email = request.form.get('email','')
        user.phonenumber = request.form.get('phonenumber','')

        try:
            db.session.add(user)
            db.session.commit()
        except:
            print("**************************")
            print("skrskrskr")
            print("**************************")
        else:
            print("***************************")
            print("666666666666666666666666666")
            print("****************************")

        return redirect('/private')


