import io
import os
import sys
import json
import torch
from torchvision import transforms
from torchvision.models import alexnet
from PIL import Image
from flask import Flask, request
from torchvision import datasets

model = None


def handler(event, context=None):
    # Download dataset
    start = GetTime()
    size = 1000
    test_dataset = datasets.CIFAR10(root='./data', train=False, transform=transform, download=True)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
    latency = (GetTime()-start)*1000
    return latency



app = Flask(__name__)

@app.route('/event-invoke', methods = ['POST'])
def invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    event = {}
    result = handler(event)
   # print(result)
    return "Finished!" + "计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"


@app.route('/web-invoke/python-flask-http', methods = ['POST','GET'])
def web_invoke():
    startTime = GetTime()
    loopTime = 10000000
     # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    event = {}
    result = handler(event)
    retTime = GetTime()
    return {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": temp,
    }
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)