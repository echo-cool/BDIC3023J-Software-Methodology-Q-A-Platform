import json
import os
import threading
import time

import requests
from flask import Response
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from app import create_app, db, admin
from app.models import User, Role, Students, Permission, Post, Comment, Like, Notification, Transaction, Activity

# if you want to execute the program
# please run this file

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db, render_as_batch=True)
from geetest_config import GEETEST_ID, GEETEST_KEY, REDIS_HOST, REDIS_PORT, CYCLE_TIME, BYPASS_URL, \
    GEETEST_BYPASS_STATUS_KEY

from sdk.geetest_lib import GeetestLib




geetest_dict = {}


# 发送bypass请求，获取bypass状态并进行缓存
def check_bypass_status():
    response = ""
    params = {"gt": GEETEST_ID}
    try:
        response = requests.get(url=BYPASS_URL, params=params)
    except Exception as e:
        print(e)
    if response and response.status_code == 200:
        print(response.content)
        bypass_status_str = response.content.decode("utf-8")
        bypass_status = json.loads(bypass_status_str).get("status")
        geetest_dict[GEETEST_BYPASS_STATUS_KEY] = bypass_status
    else:
        bypass_status = "fail"
        geetest_dict[GEETEST_BYPASS_STATUS_KEY] = bypass_status
    print("bypass状态已经获取并存入redis，当前状态为-{}".format(bypass_status))


check_bypass_status()


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Students=Students, Permission=Permission, Post=Post,
                Comment=Comment, Like=Like, Notification=Notification, Transaction=Transaction, Activity=Activity)


# 从缓存中取出当前缓存的bypass状态(success/fail)
def get_bypass_cache():
    bypass_status_cache = geetest_dict[GEETEST_BYPASS_STATUS_KEY]
    bypass_status = bypass_status_cache
    return bypass_status


# 验证初始化接口，GET请求
@app.route("/auth/register_check", methods=["GET"])
def first_register():
    # 必传参数
    #     digestmod 此版本sdk可支持md5、sha256、hmac-sha256，md5之外的算法需特殊配置的账号，联系极验客服
    # 自定义参数,可选择添加
    #     user_id 客户端用户的唯一标识，确定用户的唯一性；作用于提供进阶数据分析服务，可在register和validate接口传入，不传入也不影响验证服务的使用；若担心用户信息风险，可作预处理(如哈希处理)再提供到极验
    #     client_type 客户端类型，web：电脑上的浏览器；h5：手机上的浏览器，包括移动应用内完全内置的web_view；native：通过原生sdk植入app应用的方式；unknown：未知
    #     ip_address 客户端请求sdk服务器的ip地址
    bypass_status = get_bypass_cache()
    gt_lib = GeetestLib(GEETEST_ID, GEETEST_KEY)
    digestmod = "md5"
    user_id = "test"
    param_dict = {"digestmod": digestmod, "user_id": user_id, "client_type": "web", "ip_address": "127.0.0.1"}
    if bypass_status == "success":
        result = gt_lib.register(digestmod, param_dict)
    else:
        result = gt_lib.local_init()
    # 注意，不要更改返回的结构和值类型
    return Response(result.data, content_type='application/json;charset=UTF-8')


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file('favicon.ico')


# thread = threading.Thread(target=check_bypass_status)
# thread.start()
# app.secret_key = GeetestLib.VERSION

# User, Role, Students, Permission, Post, Comment, Like, Notification, Transaction, Activity
# admin.add_view(ModelView(User, db.session, name="Users", endpoint="users"))
# admin.add_view(ModelView(Role, db.session, name="roles", endpoint="roles"))
# admin.add_view(ModelView(Students, db.session, name="Studentss", endpoint="Studentss"))
# # admin.add_view(ModelView(Permission, db.session, name="Permissions", endpoint="Permissions"))
# admin.add_view(ModelView(Post, db.session, name="Posts", endpoint="Posts"))
# admin.add_view(ModelView(Comment, db.session, name="Comments", endpoint="Comments"))
# admin.add_view(ModelView(Like, db.session, name="Likes", endpoint="Likes"))
# admin.add_view(ModelView(Notification, db.session, name="Notifications", endpoint="Notifications"))
# admin.add_view(ModelView(Transaction, db.session, name="Transactions", endpoint="Transactions"))
# admin.add_view(ModelView(Activity, db.session, name="Activities", endpoint="Activities"))
# admin.add_view(FileAdmin("."))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
