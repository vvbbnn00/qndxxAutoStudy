# 青年大学习自动学习脚本

[![Learn](https://github.com/vvbbnn00/qndxxAutoStudy/actions/workflows/autoLearn.yml/badge.svg)](https://github.com/vvbbnn00/qndxxAutoStudy/actions/workflows/autoLearn.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/12c954d862304accb60f088f29fab550)](https://app.codacy.com/gh/vvbbnn00/qndxxAutoStudy/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![GitHub License](https://img.shields.io/github/license/vvbbnn00/qndxxAutoStudy)

> 本项目仅供学习交流使用，不得用于商业用途，因使用本项目导致的任何后果，与本人无关。

## 说明

本脚本用于自动完成青年大学习的学习任务，在进行简单的初始化后，您便可摆脱每周的青年大学习打卡的束缚。请注意，本脚本仅
适用于 **上海地区** 、且平台为微信公众号 **青春上海** 的青年大学习任务。若您需要本地使用，则在使用本脚本前，请先保证您
的计算机中已安装 **Python3.6** 或以上版本的Python环境。若您选择 **更快的快速上手** 部署项目，则无需安装Python。

## 更快的快速上手

该章节适用于**已经关注了`青春上海`微信公众号**、**已在公众号中留有学习记录**且**没有更改姓名、学号等需求**的用户。
通过本章节的配置，可以让您直接使用`GitHub`中的`Actions`功能自动学习，关于这一部分内容详见
**[GitHub Actions](#推荐-github-actions)**。

1、访问[https://vvbbnn00.github.io/qndxxAutoStudy/](https://vvbbnn00.github.io/qndxxAutoStudy/)，
微信扫码，记录下获取到的`Token`。

2、Fork该项目，接着，在项目的`Settings`-`Secrets and variables`-`Actions`-`Repository secrets`处新建一个`Secret`（点击New
repository secret），
名称为`KEY`，内容是获取到的`Token`。

3、若您是初次配置，请至`Actions`，点击`I understand my workflows, go ahead and enable
them`启用`Actions`，在左侧面板找到`Learn`，点击`Enable`启用该任务。

Enjoy🎉

## 快速上手（本地部署）

在使用之前，请确保学习用的微信账号**已经关注了`青春上海`微信公众号**，这十分重要！

1、安装必须的Python库

```bash
pip install -r requirements.txt
```

2、运行Flask服务器，请注意，host需要设置为局域网设备可访问的IP而非`127.0.0.1`，port可以自行设置

```bash
flask run --host=0.0.0.0 --port=11451
```

或者

```bash
python app.py
```

3、使用桌面端浏览器访问`http://<host>:<port>/`，并按照提示使用微信扫码登录

4、复制`1、调用脚本`中的Token

5、在计算机上运行脚本

```bash
python script.py [获取的Token]
```

## 详细说明

### 脚本文件说明

`script.py`是主要的脚本文件，用于完成青年大学习的学习任务。

#### 主要参数

| 参数     | 说明                  |
|--------|---------------------|
| <登录信息> | 登录信息，获取方式见README.md |

#### 可选参数

| 参数                     | 含义              | 说明                                                                                        |
|------------------------|-----------------|-------------------------------------------------------------------------------------------|
| -v, --version          | /               | 输出当前版本号，然后退出程序                                                                            |                     
| -h, --help             | /               | 显示帮助并退出                                                                                   |
| -o, --orgId            | 自定义组织ID         | 可选，输入此项后，学习记录的组织ID将被替换为此项的值，若不填写，则默认为最后一次学习的组织ID                                          |
| -n, --name             | 姓名/学号/工号        | 可选，输入此项后，您的姓名/学号/工号将被替换为此项的值，若不填写，则默认为最后一次学习的信息                                           |
| -so, --subOrg          | 子区域             | 可选，输入此项后，您的子区域信息将被替换为此项的值，若不填写，则默认为最后一次学习的信息，该项仅在四级组织需手动填写时需要填写，若四级组织存在，则请勿填写此项，会导致学习失败   |
| -a, --onAction         | GitHub Action模式 | 该选项表示您正在以GitHub Action环境执行自动学习任务，由于在Public仓库中，所有的Action都会留下日志，因此，当启用该选项后，将不会在控制台输出任何个人信息。 |
| -wx, --wechatWebhook   | 企业微信Webhook地址   | 可选，输入此选项后，在学习结束时，会自动向绑定的企业微信机器人发送消息通知。                                                    |
| -dd, --dingdingWebhook | 钉钉Webhook地址     | 可选，输入此选项后，在学习结束时，会自动向绑定的钉钉机器人发送消息通知。                                                      |
| -p, --proxy            | 是否启用代理          | 启用该选项后，会自动获取可用代理，并通过代理发送请求                                                                |
| -s, --savePic          | 是否保存学习完成截图      | 启用该选项后，会在学习完成后保存学习完成截图，截图保存在`./qndxximg/`目录下，文件名为`endimg_{时间戳}.jpg`，若不启用该选项，则不会保存截图。      |

#### 例子

使用最后一次学习的信息完成新的学习任务

```bash
python script.py 1234567890abcdef
```

使用自定义信息完成新的学习任务

```bash
python script.py 1234567890abcdef -o N0001 -n "张三" -so "子区域1"
```

### Flask应用说明

Flask应用的端口可以随意更改，但开放Host必须能够从局域网访问到。在微信扫码成功获取登录信息后，若没有额外需求，
可以直接关闭Flask应用，登录信息是**长期有效**的，在青春上海平台更新前，不需要担心登录信息失效。

#### 获取登录信息

流程同`快速上手`中的`3、使用桌面端浏览器访问`。

#### 登录结果页面

`登录结果`页面提供了3种完成学习的方式，第一种是使用`script.py`脚本完成学习，第二种和第三种则为访问`Flask应用`相应URL的方式。

第一种方式在`1、调用脚本`和`脚本文件说明`中已经介绍过，这里不再赘述。

第二种方式如页面中介绍，扫描`登录结果`页面`2、访问URL`下方的二维码即可完成学习，
该链接长期有效，您可收藏后多次使用，默认以最后一次完成的组织信息完成最新一期的青年大学习，
若您在过去从未在青春上海平台完成青年大学习，则需使用第三种方式。

第三种方式如页面中介绍，在`登录结果`页面`3、自定义URL`下方，选择您需要完成学习的组织，
并填入您的姓名，点击`生成链接`获取学习链接，扫码即可完成学习。该链接长期有效，您可收藏后多次使用。

## 进阶

### 定时触发

正如文档中描述，无论是脚本还是Flask应用执行学习任务，都是运行一次后立即停止的，若您需要定时触发学习任务，
则需要自行编写定时任务。

#### **[推荐] GitHub Actions**

使用GitHub Actions来完成自动学习任务是被推荐的。这是一种相对而言最为方便的方式。目前的Action配置文件是
[autoLearn.yml](.github/workflows/autoLearn.yml)，默认启用了`GitHub Action模式`，预留企业微
信Webhook配置变量，每周二11时30分自动启动学习。您可以根据自己的情况进行相应的调整。

要使用Github Actions，您首先需要`fork`该项目，接着，在项目的`Settings`-`Actions secrets and
variables`-`Actions`-`Secrets`处新建两个Secret，名称和相应内容如下表

| 键 (Key)          | 值 (Value)                    |
|------------------|------------------------------|
| KEY              | 您获取到的Token，如果还未获取，请参考说明的前半部分 |
| WECHAT_WEBHOOK   | [可选的] 您的企业微信机器人Webhook地址     |
| DINGDING_WEBHOOK | [可选的] 您的钉钉机器人Webhook地址       |

接着，若您是初次配置，请至`Actions`，点击`I understand my workflows, go ahead and enable
them`启用`Actions`，在左侧面板找到`Learn`，点击`Enable`启用该任务。

大功告成🎉

##### 手动运行学习任务

在`Actions`-`Learn`中，点击`Run Workflow`，即可手动运行一次学习任务。

##### 删除学习任务

若您需要删除学习任务，同样地，在`Actions`-`Learn`中，点击右上角的`...`，点击`Disable Workflow`即可。

#### Linux 或 Windows

Linux下可以使用`crontab`命令来编写定时任务，Windows下可以使用`计划任务`来编写定时任务，具体使用方法请自行搜索。

### docker
在目录运行
```sh
 docker-compose up -d
```

### 消息推送

**该功能仅通过`script.py`调用时有效。**

若您需要第一时间收到学习完毕的消息，则可以配置消息推送功能。目前支持的消息推送平台只有`企业微信、钉钉`，若有更多需求，
可发`issue`，由于本人比较忙，更新较慢，请见谅。

#### 企业微信

配置企业微信消息通知十分简单，只需要在执行脚本时添加参数`-wx=你的机器人Webhook地址`。

`机器人Webhook地址`可以通过在企业微信中新建一个群聊，接着点击右上角`...`，选择`群机器人`-`添加`即可。

#### 钉钉

配置钉钉消息通知十分简单，只需要在执行脚本时添加参数`-dd=你的机器人Webhook地址`。

`机器人Webhook地址`可以通过在钉钉中新建一个群聊，接着点击右上角齿轮，选择`机器人`-`添加机器人`-`自定义`。
安全设置选择`自定义关键词`，关键词填写`青年大学习`，接着点击`完成`即可。

### 代理

若您的网络环境需要使用代理才能访问外网，则需在`config/api_config.py`中配置代理信息。

```python
# 代理配置
PROXY = {
    "http": "http://...",
    "https": "https://..."
}
```

除了上述方法之外，您还可以在执行脚本时添加参数`-p`或`--proxy`来启用代理，启用该选项后，会自动获取可用代理，并通过代理发送请求。

由于公用代理IP池的不稳定性，您可以通过修改`config/api_config.py`中的`PROXY_POOL_URL`来更换代理IP池。

本项目的IP池基于[ProxyPool](https://github.com/jhao104/proxy_pool)搭建，感谢该项目作者。

## 免责声明

本项目仅供学习交流使用，不得用于商业用途，因使用本项目导致的任何后果，与本人无关。
