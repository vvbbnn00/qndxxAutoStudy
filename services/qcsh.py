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
import time
from urllib.parse import urljoin

import requests

from config.api_config import QCSH_AREA_LIST_URL, QCSH_STUDY_INFO_URL, QCSH_STUDY_URL, QCSH_STUDY_LAST_INFO_URL, \
    QCSH_TOKEN_URL, USER_AGENT
from config.patterns import PATTERN_accessToken


def getChildrenNode(pid):
    """
    获取子节点
    """
    ret = requests.get(QCSH_AREA_LIST_URL.format(pid=pid), headers={
        'Users-Agent': USER_AGENT
    }, proxies=PROXY, timeout=120)
    ret_json = ret.json()
    return ret_json.get("result")


class QcshService:
    access_token: str

    def __init__(self, access_token, proxy=None):
        self.access_token = access_token
        global PROXY
        if proxy is not None:
            PROXY = proxy
        else:
            PROXY = None

    def login(self, login_data):
        """
        通过LoginData登录青年大学习
        :param login_data: 登录信息
        """
        open_id = login_data.get("openid")
        nickname = login_data.get("nickname")
        avatar = login_data.get("headimg")
        ret = requests.get(QCSH_TOKEN_URL.format(open_id=open_id,
                                                 nickname=nickname,
                                                 avatar=avatar),
                           headers={
                               'Users-Agent': USER_AGENT
                           },
                           proxies=PROXY,
                           timeout=120)
        r = re.findall(PATTERN_accessToken, ret.text)
        self.access_token = r[0] if len(r) > 0 else None
        return self.access_token

    def getLatestInfo(self):
        """
        获取最新的学习ID
        """
        ret = requests.get(QCSH_STUDY_INFO_URL.format(access_token=self.access_token), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY, timeout=120)
        ret_json = ret.json()
        return ret_json.get("result")[0].get("id")

    def getLatestEndPicURL(self):
        """
        获取最新的学习完成截图URL
        """
        ret = requests.get(QCSH_STUDY_INFO_URL.format(access_token=self.access_token), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY, timeout=120)
        ret_json = ret.json()
        url = ret_json.get("result")[0].get("uri")
        if url is None:
            return None
        return urljoin(url, "images/end.jpg")

    def downloadEndPic(self):
        """
        下载学习完成截图
        """
        pic_url = self.getLatestEndPicURL()
        if pic_url is None:
            return False, '未找到截图URL'
        timestamp = int(time.time() * 1000)
        local_path = f"qndxximg/endimg_{timestamp}.jpg"
        response = requests.get(pic_url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.content)
            return True, local_path
        else:
            return False, pic_url

    def updateStudyRecord(self, pid, student_number, subOrg=None):
        """
        更新学习记录
        """
        ret = requests.post(QCSH_STUDY_URL.format(access_token=self.access_token), headers={
            'Users-Agent': USER_AGENT
        }, json={
            "course": self.getLatestInfo(),
            "subOrg": subOrg,
            "nid": pid,
            "cardNo": student_number}, proxies=PROXY, timeout=120)
        ret_json = ret.json()
        if ret_json.get("status") == 200:
            return True, json.dumps(ret_json.get("result"), ensure_ascii=False)
        # logging.error("学习失败：" + json.dumps(ret_json, ensure_ascii=False))
        return False, json.dumps(ret_json, ensure_ascii=False)

    def getLastStudyInfo(self):
        """
        获取最后一次学习记录
        """
        ret = requests.get(QCSH_STUDY_LAST_INFO_URL.format(access_token=self.access_token), headers={
            'Users-Agent': USER_AGENT
        }, proxies=PROXY, timeout=120)
        ret_json = ret.json()
        if ret_json.get('status') != 200:
            logging.error("获取学习记录失败：" + json.dumps(ret_json, ensure_ascii=False))
            return None
        return ret_json.get("result")


if __name__ == '__main__':
    print(getChildrenNode("N"))
