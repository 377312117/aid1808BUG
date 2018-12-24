'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
from datetime import datetime
import json

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from . import main
from .. import db,login_required
from ..models import *
from .getdata import get_lastdata




@main.errorhandler(404)
def page_not_found(e):
    '''用于无法找到页面时的404提示'''
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    '''用于服务器出现错误时的提示'''
    return render_template('500.html'), 500

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    '''用于抵达主页'''
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        print('存在session信息,直接登录')
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        print('存在cookies信息,直接登录')
    houses = Houses.query.all()
    return render_template('/index.html',params=locals())

@main.route('/index_list',methods=['GET','POST'])
@login_required
def index_list():
    '''用于抵达列表页'''
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        print('存在session信息,直接登录')
        return render_template('/index_list.html',uname=uname)
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        print('存在cookies信息,直接登录')
        return render_template('/index_list.html',uname=uname)

@main.route('/index_detail',methods=['GET','POST'])
@login_required
def index_detail():
    '''用于抵达详情页'''
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        print('存在session信息,直接登录')
        return render_template('/index_detail.html',uname=uname)
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        print('存在cookies信息,直接登录')
        return render_template('/index_detail.html',uname=uname)







