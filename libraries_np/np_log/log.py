import numpy as np
from flask import Flask, request

def handler(event, context=None):
    a=np.array([1.00000000e+00,8.66025404e-01,7.07106781e-01,5.00000000e-01,6.12323400e-17])
    return np.log(a)

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