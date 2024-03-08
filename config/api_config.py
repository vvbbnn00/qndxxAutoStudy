# _*_ coding: utf-8 _*_
"""
Time:     2022/9/16 20:30
Author:   不做评论(vvbbnn00)
Version:  
File:     api_config.py
Describe: 
"""

API_VERSION = "v20240309.1"
USER_AGENT = "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, " \
             "like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/5.2.380 Edg/104.0.5112.81"
PROXY = None

# 青年大学习服务确认接口地址
QCSH_CHECK_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/organization/children"
# 青年大学习区域列表接口地址
QCSH_AREA_LIST_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/organization/children?pid={pid}"
# 青年大学习获取微信信息接口地址
QCSH_OAUTH_INFO_URL = "https://wx.yunban.cn/wx/oauthInfoCallback?r_uri={local_url}&source=common"
# 获取当前最新的青年大学习活动数据
QCSH_STUDY_INFO_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/course/" \
                      "current?accessToken={access_token}"
# 青年大学习提交学习记录接口地址
QCSH_STUDY_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join?accessToken={access_token}"
# 青年大学习获取最后一次填写信息地址
QCSH_STUDY_LAST_INFO_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/last-info?" \
                           "accessToken={access_token}"
# 微信扫码登录
WECHAT_OAUTH_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa693f4127cc93fad&" \
                   "redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state=STATE&" \
                   "component_appid=wx0f0063354bfd3d19&connect_redirect=1"
# 青年大学习获取Token地址
QCSH_TOKEN_URL = "https://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback?appid=wxa693f4127cc93fad" \
                 "&openid={open_id}" \
                 "&nickname={nickname}" \
                 "&headimg={avatar}" \
                 "&callback=https%3A%2F%2Fqcsh.h5yunban.com%2Fyouth-learning%2F&scope=snsapi_userinfo"
# IP代理池地址
PROXY_POOL_URL = "https://getproxy.bzpl.tech/get/"
