"""
对整个应用做初始化操作
主要工作
    1.构建flask应用以及各种配置
    2.构建SQLALchemy的应用

"""
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    '''正则转化类,继承自BaseConverter,和基础数据类型约束具有相同格式'''

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


pymysql.install_as_MySQLdb()

# 创建应用实例
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 设置启动模式为调试模式
    app.config['DEBUG'] = True # app.run(debug=True)

    # 配置数据库的连库字符串
    dbconf = "mysql+pymysql://root:123456@localhost:3306/bugproject"
    app.config['SQLALCHEMY_DATABASE_URI'] = dbconf

    # 配置自动提交的问题
    # 指定当视图执行完毕后,自动提交数据库操作,不需要commit操作:db.session.commit()
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    # 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True

    # 如果设置成 True (默认情况),Flask-SQLAlchemy将会追踪对象的修改并且发送信号。
    # 这需要额外的内存,如果不必要的可以禁用它。
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = False

    # 设置session的名字
    app.config['SECRET_KEY'] = 'gaodezufang'

    # 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: re
    app.url_map.converters['re'] = RegexConverter

    
    # 将main,users中的蓝图应用关联到app上
    from .main import main as main_blueprint
    from .users import users as users_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)

    # 数据库应用实例的初始化
    db.init_app(app)


    return app



    


# from flask_login import LoginManager

# #用户认证
# login_manger=LoginManager()



# #配置用户认证信息
# login_manger.init_app(app)
# #认证加密程度
# login_manger.session_protection='strong'
# #登陆认证的处理视图
# login_manger.login_view='auth.login'
# #登陆提示信息
# login_manger.login_message=u'对不起，您还没有登录'
# login_manger.login_message_category='info'


from functools import wraps
from flask import session,request,redirect
#func是使用该修饰符的地方是视图函数
def login_required(func):
    @wraps(func)
    def intercept(*args,**kwargs):
        
        #现在是模拟登录，获取用户名，项目开发中获取session
        username = session.get('uname','')
        upassword = session.get('upwd','')

        #判断用户名存在且用户名是什么的时候直接那个视图函数
        if (username and upassword)or(request.cookies.get('uname','') and request.cookies.get('upwd','')):
            return func(*args,**kwargs)
        else:
            #如果没有就重定向到登录页面
            return redirect("/login")
    return intercept
