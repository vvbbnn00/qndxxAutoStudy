# _*_ coding: utf-8 _*_
"""
Time:     2022/9/16 21:05
Author:   不做评论(vvbbnn00)
Version:  
File:     qcsh.py
Describe: 
"""
import json
import logging
import os
import re

import requests

from config.api_config import *
from config.patterns import PATTERN_accessToken
from urllib.parse import urljoin


def getChildrenNode(pid):
    ret = requests.get(QCSH_AREA_LIST_URL.format(pid=pid), headers={
        'Users-Agent': USER_AGENT
    }, proxies=PROXY)
    ret_json = ret.json()
    return ret_json.get("result")


class QcshService:
    accessToken: str

    def __init__(self, access_token, proxy=None):
        self.accessToken = access_token
        if proxy is not None:
            global PROXY
            PROXY = proxy

    def login(self, login_data):
        open_id = login_data.get("openid")
        nickname = login_data.get("nickname")
        avatar = login_data.get("headimg")
        ret = requests.get(QCSH_TOKEN_URL.format(open_id=open_id,
                                                 nickname=nickname,
                                                 avatar=avatar),
                           headers={
                               'Users-Agent': USER_AGENT
                           }, proxies=PROXY)
        r = re.findall(PATTERN_accessToken, ret.text)
        self.accessToken = r[0] if len(r) > 0 else None
        return self.accessToken

    def getLatestInfo(self):
        ret = requests.get(QCSH_STUDY_INFO_URL.format(access_token=self.accessToken), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY)
        ret_json = ret.json()
        return ret_json.get("result")[0].get("id")
    
    def getLatestURL(self):
        ret = requests.get(QCSH_STUDY_INFO_URL.format(access_token=self.accessToken), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY)
        ret_json = ret.json()
        return ret_json.get("result")[0].get("uri")
    
    def downloadEndPic(self):
        base_url = self.getLatestURL()
        local_path = "qndxximg/endimg.jpg"
        pic_url = urljoin(base_url,"images/end.jpg")
        response = requests.get(pic_url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.content)
            return True,local_path
        else:
            return False,pic_url


    def updateStudyRecord(self, pid, student_number, subOrg=None):
        ret = requests.post(QCSH_STUDY_URL.format(access_token=self.accessToken), headers={
            'Users-Agent': USER_AGENT
        }, json={
            "course": self.getLatestInfo(),
            "subOrg": subOrg,
            "nid": pid,
            "cardNo": student_number}, proxies=PROXY)
        ret_json = ret.json()
        if ret_json.get("status") == 200:
            return True, json.dumps(ret_json.get("result"), ensure_ascii=False)
        # logging.error("学习失败：" + json.dumps(ret_json, ensure_ascii=False))
        return False, json.dumps(ret_json, ensure_ascii=False)

    def getLastStudyInfo(self):
        ret = requests.get(QCSH_STUDY_LAST_INFO_URL.format(access_token=self.accessToken), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY)
        ret_json = ret.json()
        if ret_json.get('status') != 200:
            logging.error("获取学习记录失败：" + json.dumps(ret_json, ensure_ascii=False))
            return None
        return ret_json.get("result")


if __name__ == '__main__':
    print(getChildrenNode("N"))
