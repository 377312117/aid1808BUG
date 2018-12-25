"""
管理应用的管理文件 
"""

'''
下列应用用于执行数据迁移以及在终端中执行数据库操作
'''
from flask_migrate import Migrate, MigrateCommand
# prompt_bool是用于删除数据库之前的提示,
from flask_script import Manager, Shell, prompt_bool
import os

from app.main.getdata import get_lastdata



from app import create_app,db

app = create_app()



#让python支持命令行工作
manager = Manager(app)
 
#使用migrate绑定app和db
migrate = Migrate(app,db)
 
#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)


#创建数据库
@manager.command
def create():
    db.create_all()
    return '数据库已创建'

#删除数据库
@manager.command
def drop():
    if prompt_bool('确定要删除数据库然后跑路吗？(确定请键入y)'):
        db.drop_all()
        return '数据库删除完成'
    return '删除需谨慎！'


# 爬取数据装入数据库
@manager.command
def crawling(): 
    print('获取数据中')
    get_lastdata()
    print('获取完成')

# 删除下载文件夹中所有的照片

@manager.command
def del_downloads():
    abspath = os.path.dirname(os.path.abspath(__file__))
    path =  abspath+ r'/static/images/downloads/'
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_downloads(c_path)
        else:
            os.remove(c_path)

if __name__ == '__main__':
    # 若没带命令,则会进入测试服务器环境(127.0.0.1:5000),可指定ip(-h xxxx)和端口(-p xxxx)
    manager.run()
