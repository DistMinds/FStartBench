from flask import Flask, request
import time
import os
import random
from multiprocessing import Process, Pipe

app = Flask(__name__)

@app.route('/event-invoke', methods = ['POST'])
def invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)

    event = request.get_data()
    event_str = event.decode("utf-8")

    return "Hello from SCF event function, your input: " + event_str + ", request_id: " + request_id + "\n"

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
    parallelIndex = 100
    temp = alu(loopTime, parallelIndex)
    retTime = GetTime()
    return {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": temp,
    }


def doAlu(times, childConn, clientId):
    a = random.randint(10, 100)
    b = random.randint(10, 100)
    temp = 0
    for i in range(times):
        if i % 4 == 0:
            temp = a + b
        elif i % 4 == 1:
            temp = a - b
        elif i % 4 == 2:
            temp = a * b
        else:
            temp = a / b
    print(times)
    childConn.send(temp)
    childConn.close()
    return temp


def alu(times, parallelIndex):
    per_times = int(times / parallelIndex)
    threads = []
    childConns = []
    parentConns = []
    for i in range(parallelIndex):
        parentConn, childConn = Pipe()
        parentConns.append(parentConn)
        childConns.append(childConn)
        t = Process(target=doAlu, args=(per_times, childConn, i))
        threads.append(t)
    for i in range(parallelIndex):
        threads[i].start()
    for i in range(parallelIndex):
        threads[i].join()
    
    results = []
    for i in range(parallelIndex):
        results.append(parentConns[i].recv())
    return str(results)


def GetTime():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
