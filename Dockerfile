# 使用官方Python运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到位于/app中的容器中
COPY . /app

# 安装requirements.txt中指定的任何所需包
# 确保requirements.txt中包括gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# 使端口11451可用于网络之外的通信
EXPOSE 11451

# 环境变量设置为告诉gunicorn命令在哪里找到应用
ENV FLASK_APP=app.py

# 在容器启动时使用Gunicorn运行Flask应用
CMD ["gunicorn", "--bind", "0.0.0.0:11451", "app:app"]
