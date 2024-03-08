# _*_ coding: utf-8 _*_
"""
Time:     2022/9/16 20:09
Author:   不做评论(vvbbnn00)
Version:  
File:     debug.py
Describe: 
"""
import json

from flask import Flask, request, render_template, url_for
from config.api_config import QCSH_OAUTH_INFO_URL, WECHAT_OAUTH_URL, API_VERSION
import base64

from services.qcsh import getChildrenNode, QcshService

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", qr_data=WECHAT_OAUTH_URL
                           .format(redirect_uri=QCSH_OAUTH_INFO_URL
                                   .format(local_url=url_for("qr", _external=True))), version=API_VERSION)


@app.route('/qr')
def qr():
    query_args = request.args
    login_data = base64.b64encode(json.dumps(dict(query_args)).encode()).decode()
    return render_template("result.html",
                           nickname=query_args.get("nickname"),
                           avatar=query_args.get("headimg"),
                           login_data=login_data,
                           base_url=url_for("study", _external=True))


@app.route('/orgInfo')
def orgInfo():
    node = "N" if request.args.get("pid") is None else request.args.get("pid")
    return getChildrenNode(node)


@app.route('/study')
def study():
    try:
        login_data = json.loads(base64.b64decode(request.args.get("data")).decode())
    except Exception as e:
        return render_template("study.html", study_result="学习失败",
                               msg="登录信息有误，请重新扫码登录")
    qcshService = QcshService('')
    ret = qcshService.login(login_data)
    if ret is None:
        return render_template("study.html", study_result="学习失败",
                               msg="登录失败，请重新扫码登录")
    card_no = request.args.get("name")
    nid = request.args.get("orgCode")
    sub_org = request.args.get("subOrg")

    if card_no is None or nid is None:
        last_study_info = qcshService.getLastStudyInfo()
        if last_study_info is None:
            return render_template("study.html", study_result="学习失败",
                                   msg="未查询到您最后一次的学习记录，请先在微信“青年大学习”页面完成一次学习，或使用“自定义URL”提交学习请求")
        card_no = last_study_info.get("cardNo")
        nid = last_study_info.get("nid")
        sub_org = last_study_info.get("subOrg")

    success, study_result = qcshService.updateStudyRecord(nid, card_no, sub_org)
    if not success:
        return render_template("study.html", study_result="学习失败",
                               msg="学习失败，请重新扫码登录", data=study_result)
    return render_template("study.html", study_result="学习成功", msg="您已完成学习，可在微信“青年大学习”页面查看学习记录",
                           data=study_result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=11451)
