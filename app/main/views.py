'''
此模块用于配置路由映射函数以及反馈给客户端的视图
'''

import os
import random
import urllib.parse
from datetime import datetime
import json

from flask import Flask, redirect, render_template, request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

from . import main
from .. import db,login_required
from ..models import *




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
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在session信息,直接登录')
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在cookies信息,直接登录')

    # Alex：如果查询历史中有信息，就根据信息查询
    low_price = session.get("low_price",0)
    high_price = session.get("high_price",30000)
    district = session.get("district","")
    # zzx:修改为下面这行即可统计数据
    count = Houses.query.count()
    # print('count:',count)
    if  low_price or high_price or district:
        if not district:
            houses = list(Houses.query.filter(Houses.price < high_price, Houses.price > low_price).all())
        else:
            # 优先district
            houses = list(Houses.query.filter(Houses.district.like(district + '%'),Houses.price < high_price,Houses.price > low_price).all())


        houses1 = random.sample(houses,4)

        houses2 = random.sample(houses,4)

        houses3 = random.sample(houses,5)

    # alex:index二次修改结束
    else:
        l1 = [random.randint(1,count//2) for _ in range(4)]
        houses1 = Houses.query.filter(Houses.id.in_(l1)).all()

        l2 = [random.randint(1, count//2) for _ in range(8)]
        houses2 = Houses.query.filter(Houses.id.in_(l2)).all()

        l3 = [random.randint(count//2,count) for _ in range(5)]
        houses3 = Houses.query.filter(Houses.id.in_(l3)).all()


    return render_template('/index.html',params=locals())

@main.route('/index_list',methods=['GET','POST'])
@login_required
def index_list():
    '''用于抵达列表页'''

    # alex:第一次修改，主页的搜索框
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在session信息,直接登录')
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在cookies信息,直接登录')

    if request.method == 'GET':
        com = request.args.get("com",'')
        pn = request.args.get("pn",1,type=int)
        high_price = request.args.get('high_price',500,type=int)
        low_price = request.args.get('low_price',30000,type=int)

        if pn == 0:
            pn = 1

        if com == "default":
            if "district" in session:
                houses = Houses.query.filter(Houses.district.like(session['district'] + '%'), Houses.price > session['low_price'],Houses.price < session['high_price']).paginate(page=pn, per_page=9,error_out=False).items
            else:
                # l = [random.randint(1,Houses.query.count()) for _ in range(9)]
                # houses = Houses.query.filter(Houses.id.in_(l)).all()
                houses = Houses.query.paginate(page=pn,per_page=9,error_out=False).items
        elif com == "1":
            if "district" in session:
                houses = Houses.query.filter(Houses.district.like(session['district'] + '%'),
                                             Houses.price > session['low_price'],
                                             Houses.price < session['high_price']).order_by(db.desc(Houses.price)).paginate(page=pn, per_page=9,error_out=False).items
            else:
                houses = Houses.query.order_by(db.desc(Houses.price)).paginate(page=pn, per_page=9, error_out=False).items
        elif com == "0":
            if "district" in session:
                houses = Houses.query.filter(Houses.district.like(session['district'] + '%'),
                                             Houses.price > session['low_price'],
                                             Houses.price < session['high_price']).order_by(Houses.price).paginate(page=pn, per_page=9,error_out=False).items
            else:
                houses = Houses.query.order_by(Houses.price).paginate(page=pn, per_page=9, error_out=False).items
        elif com == "his":
            history_houses = Users.query.filter_by(id=session['uid']).first().history_houses.distinct().all()[-1:-5:-1]

            if "district" in session:
                houses = list(history_houses) + Houses.query.filter(Houses.district.like(session['district'] + '%'),
                                             Houses.price > session['low_price'],
                                             Houses.price < session['high_price']).order_by(Houses.price).paginate(
                    page=pn, per_page=9, error_out=False).items

            else:
                houses = list(history_houses) + Houses.query.order_by(Houses.price).paginate(page=pn, per_page=9, error_out=False).items
        elif com == "coll":
            favor_houses = Users.query.filter_by(id=session['uid']).first().favor_houses.distinct().all()[-1:-5:-1]

            if "district" in session:
                houses = list(favor_houses) + Houses.query.filter(Houses.district.like(session['district'] + '%'),
                                             Houses.price > session['low_price'],
                                             Houses.price < session['high_price']).order_by(Houses.price).paginate(
                    page=pn, per_page=9, error_out=False).items
            else:
                houses = list(favor_houses) + Houses.query.order_by(Houses.price).paginate(page=pn, per_page=9, error_out=False).items

    else:
        district = request.form.get("Location", "")
        high_price = request.form.get("high_price",500,type=int)
        low_price = request.form.get("low_price",30000,type=int)
        pn = 1
        com = "default"

        if district:
            houses = Houses.query.filter(Houses.district.like(district + '%'), Houses.price >= low_price,Houses.price <= high_price).all()

            print("*******************************")
            print(houses)
            print(district)
            print(high_price)
            print(low_price)
            print("*******************************")

            if len(houses):
                message = "为您查询到满足条件的以下房屋信息"
                print(message)
                houses = Houses.query.filter(Houses.district.like(district + '%'),Houses.price >= low_price,
                                             Houses.price <= high_price).paginate(page=pn,per_page=9,error_out=False).items
                session['district'] = houses[0].district
                session['low_price'] = low_price
                session['high_price'] = high_price
            else:
                message = "没有为您找到符合条件的房屋信息，为您做如下推荐"
                print(message)
                # houses = Houses.query.filter(Houses.id.in_([random.randint(1, Houses.query.count()) for _ in range(9)]))
                houses = Houses.query.paginate(page=pn,per_page=9,error_out=False).items


        else:
            message = "没有找到符合条件的房屋信息，为您做如下推荐"
            print(message)
            # houses = Houses.query.filter(Houses.id.in_([random.randint(1, Houses.query.count()) for _ in range(9)]))
            houses = Houses.query.paginate(page=pn,per_page=9,error_out=False).items




    return render_template('/index_list.html',params=locals())

@main.route('/index_detail',methods=['GET','POST'])
@login_required
def index_detail():
    '''用于抵达详情页'''
    if session.get('uname','') and session.get('upwd',''):
        uname = session.get('uname','')
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在session信息,直接登录')
        
    elif request.cookies.get('uname','') and request.cookies.get('upwd',''):
        session['uname']=request.cookies.get('uname','')
        session['upwd']=request.cookies.get('upwd','')
        uname = session['uname']
        user = Users.query.filter_by(name=uname).first()
        session['uid'] = user.id
        print('存在cookies信息,直接登录')

    if request.method == "GET":
        id = request.args.get("id")

        house = Houses.query.filter_by(id=id).first()

        history = History.query.filter_by(user_id = session['uid'],house_id=id).first()

        # 加入历史记录
        history = History(user_id=session['uid'],house_id=id,pub_date=datetime.now())

        try:
            db.session.add(history)
            db.session.commit()
        except:
            print("插入数据失败")
        else:
            print("插入数据成功")


        favor = Favor.query.filter_by(user_id=session['uid'],house_id=id).all()

        if favor:
            msg = "collected"
        else:
            msg = "爸爸好累"


        if session.get('district',''):
            houses = Houses.query.filter(Houses.district.like(session['district'] + '%'), Houses.price > session['low_price'], Houses.price < session['high_price']).distinct().limit(3)
        else:
            houses = houses = Houses.query.filter(Houses.id.in_([random.randint(1, Houses.query.count()) for _ in range(3)]))


        return render_template("/index_detail.html",params=locals())


@main.route('/favor')
@login_required
def favor_views():
    id = request.args.get('id')
    uid = session['uid']

    favors = Favor.query.filter_by(user_id=uid,house_id=id).all()

    if favors:
        dic = {
            "status": 0,
            "info": "取消收藏成功！"
        }

        try:
            for favor in favors:
                db.session.delete(favor)
                db.session.commit()
        except:
            dic = {
                "status": 2,
                "info": "取消收藏失败！"
            }
    else:
        favor = Favor(user_id=uid, house_id=id, pub_date=datetime.now())

        dic = {
            'status': 1,
            'info': '收藏成功!',
        }

        try:
            db.session.add(favor)
            db.session.commit()
        except:
            dic = {
                'status': 3,
                'info': '收藏失败!',
            }
    return json.dumps(dic)













