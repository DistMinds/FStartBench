FROM python:3.9-slim

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install torch==1.9.0 torchvision==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python", "-u", "./app.py" ]

