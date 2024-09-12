FROM golang:1.23-bullseye
# 安装 curl
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 添加 NodeSource PPA 并安装 Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建应用程序目录
WORKDIR /opt/src/app

# 安装应用程序依赖
# 使用通配符确保 package.json 和 package-lock.json（如果存在）都被复制
COPY package*.json ./

# 安装 npm 依赖
RUN npm install --production

# 复制应用程序源代码
COPY . .

# 监听 HTTP 服务器端口 
EXPOSE 9000

# 设置默认命令
ENTRYPOINT ["node", "server.js"]


