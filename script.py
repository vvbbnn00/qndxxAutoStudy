# _*_ coding: utf-8 _*_
"""
Time:     2022/9/17 01:02
Author:   不做评论(vvbbnn00)
Version:  
File:     script.py
Describe: 
"""
import argparse
import base64
import json
import sys
import logging

from config.api_config import API_VERSION
from services.messagePush import wechatMessagePush, dingdingMessagePush
from services.qcsh import QcshService
from services.proxies import get_available_proxy

logging.getLogger().setLevel(logging.INFO)
VERSION = API_VERSION


def doStudy():
    """
    执行学习任务
    :return:
    """
    logging.info('开始学习...')

    # 按情况获取代理
    if args.proxy:
        proxy = get_available_proxy(onAction=args.onAction)
    else:
        proxy = None

    qcshService = QcshService('', proxy=proxy)
    try:
        login_data = json.loads(base64.b64decode(args.login_data[0]))
    except Exception:
        logging.error('登录信息解析失败，请检查登录信息是否正确')
        return False, '登录信息解析失败，请检查登录信息是否正确'

    ret = qcshService.login(login_data)
    if ret:
        if args.onAction:  # 消除敏感信息
            ret = "***"
        logging.info('登录成功, AccessToken=' + ret)
    else:
        logging.error('登录失败，请检查登录信息是否正确')
        return False, '登录失败，请检查登录信息是否正确'

    nid = args.orgId
    card_no = args.name
    subOrg = args.subOrg
    last_study_info = qcshService.getLastStudyInfo()

    if args.savePic:
        logging.info("正在尝试抓取完成截图")
        pic_success, pic_path = qcshService.downloadEndPic()
        if pic_success:
            logging.info("抓取截图成功，已经保存到当前文件夹下的 %s", pic_path)
        else:
            logging.error("抓取截图失败，获取的url为 %s", pic_path)

    if not args.onAction:
        logging.info("最后一次学习的信息如下")
        logging.info(json.dumps(last_study_info, ensure_ascii=False, indent=4))

    if nid is None:
        if last_study_info is None:
            logging.error("未找到最后一次学习的信息，无法自动获取组织ID，请手动输入组织ID")
            return False, "未找到最后一次学习的信息，无法自动获取组织ID，请手动输入组织ID"
        logging.warning('未指定组织ID，将使用最后一次学习的组织ID')
        nid = last_study_info.get("nid")
        if last_study_info.get("subOrg"):
            subOrg = last_study_info.get("subOrg")

    if card_no is None:
        if last_study_info is None:
            logging.error("未找到最后一次学习的信息，无法自动获取姓名/学号/工号，请手动输入")
            return False, "未找到最后一次学习的信息，无法自动获取姓名/学号/工号，请手动输入"
        logging.warning('未指定姓名/学号/工号，将使用最后一次学习的信息')
        card_no = last_study_info.get("cardNo")

    logging.info("正在尝试提交记录...")
    success, ret = qcshService.updateStudyRecord(nid, card_no, subOrg)
    if args.onAction:
        logging.info(f'学习{"成功" if success else "失败"}')
    else:
        logging.info(f'学习{"成功" if success else "失败"}，返回信息：{ret}')
    return success, ret, qcshService.getLatestEndPicURL()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'青年大学习自动学习脚本 版本{VERSION}')
    parser.add_argument('login_data', metavar='<登录信息>', type=str, nargs=1,
                        help='登录信息，获取方式见README.md')
    parser.add_argument('-o', '--orgId', metavar='[自定义组织ID]',
                        help='可选，输入此项后，学习记录的组织ID将被替换为此项的值，若不填写，则默认为最后一次学习的组织ID',
                        type=str, default=None)
    parser.add_argument('-n', '--name', metavar='[姓名/学号/工号]',
                        help='可选，输入此项后，您的姓名/学号/工号将被替换为此项的值，若不填写，则默认为最后一次学习的信息',
                        type=str, default=None)
    parser.add_argument('-so', '--subOrg', metavar='[子区域]',
                        help='可选，输入此项后，您的子区域信息将被替换为此项的值，若不填写，则默认为最后一次学习的信息，该项仅在四级组织'
                             '需手动填写时需要填写，若四级组织存在，则请勿填写此项，会导致学习失败',
                        type=str, default=None)
    parser.add_argument('-a', '--onAction', action='store_true', default=False,
                        help='该选项表示您正在以GitHub Action环境执行自动学习任务，由于在Public仓库中，所有的Action都会留下日志，因此，'
                             '当启用该选项后，将不会在控制台输出任何个人信息。')
    parser.add_argument('-wx', '--wechatWebhook', metavar='[企业微信Webhook地址]', default=None,
                        help='可选，输入此选项后，在学习结束时，会自动向绑定的企业微信机器人发送消息通知。')
    parser.add_argument('-dd', '--dingdingWebhook', metavar='[钉钉Webhook地址]', default=None,
                        help='可选，输入此选项后，在学习结束时，会自动向绑定的钉钉机器人发送消息通知。')
    parser.add_argument('-p', '--proxy', action='store_true', default=False,
                        help='自动从代理池中获取代理，若不指定此选项，则不使用代理')
    parser.add_argument('-s', '--savePic', action='store_true', default=False,
                        help='自动保存学习完成截图，若不指定此选项，则不保存')
    parser.add_argument('-v', '--version', help='输出当前版本号，然后退出程序', action='version',
                        version=f'青年大学习自动学习脚本 版本{VERSION}')
    args = parser.parse_args(sys.argv[1:])

    success, message, endPicUrl = doStudy()
    if args.wechatWebhook:
        wechatMessagePush(args.wechatWebhook, success, message, endPicUrl)
    if args.dingdingWebhook:
        dingdingMessagePush(args.dingdingWebhook, success, message, endPicUrl)
