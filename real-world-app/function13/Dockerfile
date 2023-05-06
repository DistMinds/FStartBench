FROM python:3.7.2-slim

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install 'protobuf~=3.19.0'
COPY . .

CMD [ "python", "-u", "./app.py" ]