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
from services.qcsh import QcshService

logging.getLogger().setLevel(logging.INFO)
VERSION = API_VERSION

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
    parser.add_argument('-v', '--version', help='输出当前版本号，然后退出程序', action='version', version=f'青年大学习自动学习脚本 版本{VERSION}')
    args = parser.parse_args(sys.argv[1:])

    logging.info('开始学习...')

    qcshService = QcshService('')
    login_data = None
    try:
        login_data = json.loads(base64.b64decode(args.login_data[0]))
    except Exception:
        logging.error('登录信息解析失败，请检查登录信息是否正确')
        exit(1)

    ret = qcshService.login(login_data)
    if ret:
        logging.info('登录成功, AccessToken=' + ret)
    else:
        logging.error('登录失败，请检查登录信息是否正确')
        exit(1)

    nid = args.orgId
    card_no = args.name
    subOrg = args.subOrg
    last_study_info = qcshService.getLastStudyInfo()
    logging.info("最后一次学习的信息如下")
    logging.info(json.dumps(last_study_info, ensure_ascii=False, indent=4))

    if nid is None:
        if last_study_info is None:
            logging.error("未找到最后一次学习的信息，无法自动获取组织ID，请手动输入组织ID")
            exit(1)
        logging.warning('未指定组织ID，将使用最后一次学习的组织ID')
        nid = last_study_info.get("nid")
        if last_study_info.get("subOrg"):
            subOrg = last_study_info.get("subOrg")

    if card_no is None:
        if last_study_info is None:
            logging.error("未找到最后一次学习的信息，无法自动获取姓名/学号/工号，请手动输入")
            exit(1)
        logging.warning('未指定姓名/学号/工号，将使用最后一次学习的信息')
        card_no = last_study_info.get("cardNo")

    logging.info("正在尝试提交记录...")
    ret = qcshService.updateStudyRecord(nid, card_no, subOrg)
    if ret:
        logging.info('学习成功，返回信息：' + json.dumps(ret, ensure_ascii=False, indent=4))
