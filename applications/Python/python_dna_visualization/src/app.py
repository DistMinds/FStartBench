import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from squiggle import transform
import requests
from flask import Flask, request
filename1 = "gene1.txt"
filename2 = "gene2.txt"
local_path = "./"

def visualize(data1, data2):
    return transform(data1) + transform(data2)

def handler(event, context=None):
    # Visualize sequences
    data1 = open(local_path + filename1, "r").read()
    data2 = open(local_path + filename2, "r").read()
    result = visualize(data1, data2)

    # Write result
    with open(local_path + "result.txt", "wb") as out:
        out.write(json.dumps(result).encode("utf-8"))

    return {
        "result": "Visualize {}+{} finished!".format(filename1, filename2)
    }
app = Flask(__name__)
@app.route('/event-invoke', methods = ['POST'])
def invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    event = {}
    result= handler(event)

    return "Hello from SCF event function, your input: " + str(result) + ", request_id: " + request_id + "\n"

@app.route('/web-invoke/python-flask-http', methods = ['POST','GET'])
def web_invoke():
    startTime = GetTime()
    loopTime = 10000000
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    
    # event = request.get_data()
    # event_str = event.decode("utf-8")

    # return "Hello from SCF Web function, your input: " + event_str + ", request_id: " + request_id + "\n"
    event = {}
    result= handler(event)
    retTime = GetTime()
    return {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": result,
    }
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)  
