# 首先使用 Alpine 3.18 作为基础镜像
FROM golang:1.23-bullseye

# 更新包列表并安装 python3 和 python3-pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /usr/src/app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置默认命令
CMD [ "python3", "-u", "./arccos.py" ]

