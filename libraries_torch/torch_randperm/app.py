import io
import os
import sys
import json
import torch
from flask import Flask, request




def handler(event, context=None):
    start =GetTime()
    size = 1000
    a = torch.randperm(4)
    
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