import os.path

import tool.common
import tool.validate
from flask import current_app
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def test():
    return tool.common.json_return('访问成功')


# 下载模型
def __init_model():
    if not os.path.exists('models'):
        #官方下载参考：https://huggingface.co/Helsinki-NLP/opus-mt-en-zh
        #           https://huggingface.co/Helsinki-NLP/opus-mt-zh-en
        url = 'http://luler.top:5244/d/%E8%BD%AF%E4%BB%B6%E6%96%87%E4%BB%B6/%E9%A2%84%E6%A3%80%E6%B5%8B%E6%A8%A1%E5%9E%8B/hello_translation/models.zip?sign=dwNEXEWUA5le3EkWWU89bbO615pGeHeoGONrTNIDP54=:0'
        target_file = 'models.zip'
        tool.common.download_file(url, target_file)
        tool.common.un_zip(target_file)
        os.unlink(target_file)


# 英文翻译成中文
def __predict_zh(text):
    __init_model()
    # 初始化预测对象
    if hasattr(current_app, 'tokenizer_zh') == False or hasattr(current_app, 'model_zh'):
        current_app.tokenizer_zh = AutoTokenizer.from_pretrained("./models/opus-mt-en-zh")
        current_app.model_zh = AutoModelForSeq2SeqLM.from_pretrained("./models/opus-mt-en-zh")
    batch = current_app.tokenizer_zh([text], return_tensors="pt")
    generated_ids = current_app.model_zh.generate(**batch)
    return current_app.tokenizer_zh.batch_decode(generated_ids, skip_special_tokens=True)[0]


# 中文翻译成英文
def __predict_eng(text):
    __init_model()
    # 初始化预测对象
    if hasattr(current_app, 'tokenizer_eng') == False or hasattr(current_app, 'model_eng'):
        current_app.tokenizer_eng = AutoTokenizer.from_pretrained("./models/opus-mt-zh-en")
        current_app.model_eng = AutoModelForSeq2SeqLM.from_pretrained("./models/opus-mt-zh-en")
    batch = current_app.tokenizer_eng([text], return_tensors="pt")
    generated_ids = current_app.model_eng.generate(**batch)
    return current_app.tokenizer_eng.batch_decode(generated_ids, skip_special_tokens=True)[0]


# 中英互译
def translate():
    field = ['to', 'text']
    param = tool.common.get_request_param(field)
    tool.validate.validate().checkData(param, {
        'to|翻译目标语言': 'required',
        'text|待翻译文本': 'required',
    })

    if param['to'] not in ['zh', 'eng']:
        raise Exception('翻译目标语言只能是:zh,eng')

    res = {}
    if param['to'] == 'zh':
        res['result'] = __predict_zh(param['text'])
    else:
        res['result'] = __predict_eng(param['text'])

    return tool.common.json_return('访问成功', res)
