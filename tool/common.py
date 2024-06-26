# 接口通用返回格式
import hashlib
import re
import zipfile
import requests
from flask import request
# from orator import DatabaseManager

import setting


def json_return(message='', info=[], code=200):
    from flask import jsonify
    return jsonify({
        'code': int(code),
        'message': message,
        'info': info,
    })


# 获取请求参数
def get_request_param(fields=[]):
    res = {}
    # get参数
    info = request.args
    if info != None:
        for key in info:
            res[key] = info[key]
    # post参数 json
    info = request.get_json(force=True, silent=True)
    if info != None:
        for key in info:
            res[key] = info[key]
    # post参数x-www-form-urlencoded/form-data
    info = request.form
    if info != None:
        for key in info:
            res[key] = info[key]
    # 筛选需要的字段
    if len(fields) > 0:
        temp = {}
        for field in fields:
            if field in res:
                temp[field] = res[field]
        res = temp

    return res


# 获取数据库连接
# def get_db():
#     return DatabaseManager(setting.DATABASES)


# 获取文件md5
def md5_file(file_path):
    md5_obj = hashlib.md5()
    with open(file_path, 'rb') as file_obj:
        md5_obj.update(file_obj.read())
    file_md5_id = md5_obj.hexdigest()
    return file_md5_id


# 结巴分析，默认过滤词云需要的词性
def jieba_word(text):
    # 过滤表情
    text = re.sub('\[.+\]', '', text)
    if text:
        import jieba.posseg
        a = jieba.posseg.cut(text)
        a = [(x.word, x.flag) for x in a if x.flag in ['n', 'nr', 'ns', 'nt', 'nz', 'an', 'a', 'i', 'v', 'vn', 'y', ]]
        a = list(map(lambda x: x[0], a))
    else:
        a = []
    return a


# 下载大文件
def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()


# 解压zip文件
def un_zip(file_name):
    zip_file = zipfile.ZipFile(file_name)
    try:
        zip_file.extractall()
    except:
        pass
    zip_file.close()
