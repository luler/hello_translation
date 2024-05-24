import os

from flask import request

from api import common_api
# from tool import jwt_tool

# 接口路由，全部写在这里
import tool.common


def add_new_routes(app):
    # 全局异常捕获处理
    @app.errorhandler(Exception)
    def errorhandler(error):
        error = str(error)
        code = 400
        if error == '授权凭证无效':
            code = 401
        return tool.common.json_return(error, [], code)

    # @app.before_first_request
    # def before_first_request_instance():
    #     os.system('orator migrate -c orator_database.py -f')

    @app.before_request
    def before_request_instance():
        pass
        # request.user_id = 0
        # path = request.path.lower()
        # if path.startswith('/api/auth'):
        #     token = request.headers.get('Authorization', '')
        #     if not token:
        #         token = tool.common.get_request_param(['token']).get('token', '')
        #     res = jwt_tool.jwt_decode(token)
        #     request.user_id = res['user_id']

    # 自定义路由
    app.add_url_rule('/api/test', view_func=common_api.test, methods=['POST', 'GET', ])
    app.add_url_rule('/api/translate', view_func=common_api.translate, methods=['POST'])
