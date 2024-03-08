# _*_ coding: utf-8 _*_
"""
Time:     2023/8/17 23:16
Author:   不做评论(vvbbnn00)
Version:
File:     proxies.py
Describe: 代理服务
"""
import logging

import requests

from config.api_config import PROXY_POOL_URL, QCSH_CHECK_URL


# IP 代理服务基于 https://github.com/jhao104/proxy_pool，有需要可以自行搭建

def getProxy(on_action=False):
    """
    获取代理
    :param on_action: 是否在执行动作
    :return:
    """
    logging.info("正在获取代理")
    try:
        ret = requests.get(PROXY_POOL_URL, timeout=30).json()
        if ret.get("code") == 0:
            logging.warning("服务端暂时没有可用的代理")
            return None
        else:
            if on_action:
                logging.info("获取到代理: ***")
            else:
                logging.info("获取到代理: %s(%s)" % (ret.get('proxy'), ret.get('region')))
            if ret.get('https'):
                return {
                    "https": ret.get('proxy')
                }
            else:
                return {
                    "http": ret.get('proxy')
                }
    except Exception as e:
        logging.error("获取代理失败: " + str(e))
        return None


def checkProxy(proxy):
    """
    检查代理是否可用
    :param proxy:
    :return:
    """
    logging.info("正在检查代理是否可用")
    try:
        ret = requests.get(QCSH_CHECK_URL, proxies=proxy, timeout=30)
        if ret.status_code == 200:
            logging.info("代理可用")
            return True
        else:
            logging.warning("代理不可用")
            return False
    except Exception as e:
        logging.error("代理不可用: " + str(e))
        return False


def getAvailableProxy(max_tries=5, on_action=False):
    """
    获取可用代理
    :param max_tries: 最大尝试次数
    :param on_action: 是否在执行动作
    :return: 可用代理
    """
    proxy = getProxy(on_action=on_action)
    if proxy is None:
        return None
    if checkProxy(proxy):
        return proxy
    else:
        if max_tries > 0:
            return getAvailableProxy(max_tries - 1, on_action=on_action)
        else:
            return None
