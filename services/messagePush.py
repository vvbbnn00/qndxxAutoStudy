# _*_ coding: utf-8 _*_
"""
Time:     2023/7/29 21:31
Author:   不做评论(vvbbnn00)
Version:
File:     messagePush.py
Describe: 消息推送服务
"""
import logging

import requests


def wechatMessagePush(webhookUrl: str, success: bool, message: str):
    """
    推送企业微信消息卡片

    :param webhookUrl: 企业微信Webhook地址
    :param success: 是否成功
    :param message: 返回消息
    :return:
    """
    messageTemplate = {
        "msgtype": "template_card",
        "template_card": {
            "card_type": "text_notice",
            "source": {
                "icon_url": "https://www.dayimen.net/Public/image/party_2.jpeg",
                "desc": "青年大学习助手",
                "desc_color": 0
            },
            "main_title": {
                "title": "任务完成",
                "desc": "定时任务已完成，以下是任务报告"
            },
            "emphasis_content": {
                "title": "学习成功" if success else "学习失败",
                "desc": "学习结果"
            },
            "quote_area": {
                "type": 0,
                "title": "返回信息",
                "quote_text": message
            },
            "horizontal_content_list": [],
            "jump_list": [],
            "card_action": {
                "type": 1,
                "url": "http://news.cyol.com/gb/channels/vrGlAKDl/index.html",
            }
        }
    }
    try:
        ret = requests.post(webhookUrl, json=messageTemplate).json()
        logging.info(f"通过企业微信通知用户，Errcode={ret.get('errcode')}")
    except Exception as e:
        logging.info("wechatMessagePush 请求失败")


def dingdingMessagePush(webhookUrl: str, success: bool, message: str):
    """
    推送钉钉消息卡片

    :param webhookUrl: 钉钉Webhook地址
    :param success: 是否成功
    :param message: 返回消息
    :return:
    """
    messageTemplate = {
        "msgtype": "markdown",
        "markdown": {
            "title": "青年大学习任务完成",
            "text": "#### [青年大学习](http://news.cyol.com/gb/channels/vrGlAKDl/index.html)任务完成\n" +
                    "![](https://www.dayimen.net/Public/image/party_2.jpeg)\n\n" +
                    "> " + ("学习成功" if success else "学习失败") + "\n\n" +
                    "> " + message + "\n"
        },
    }
    try:
        ret = requests.post(webhookUrl, json=messageTemplate).json()
        logging.info(f"通过钉钉通知用户，Errcode={ret.get('errcode')}")
    except Exception as e:
        logging.info("dingdingMessagePush 请求失败")
