from flask import Flask, request
import numpy as np
from time import time
import json
import igraph

def graph_ops(size):
    graph = igraph.Graph.Barabasi(size, 10)
    return graph.pagerank()[0]

def handler(event, context=None):
    start = time()
    size = 1000
    result = graph_ops(size)
    latency = (time() - start)*1000
    return latency
  #  return {
 #       "result": "{} size graph BFS finished!".format(size)
#    }

app = Flask(__name__)
@app.route('/event-invoke', methods = ['POST'])
def invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    event = {}
    result = handler(event)
   # print(result)
    return "1000 size graph BFS finished!" + "计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"


@app.route('/web-invoke/python-flask-http', methods = ['POST','GET'])
def web_invoke():
    startTime = GetTime()
    loopTime = 10000000
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    event = {}
    result = handler(event)
   # print(result)
    # event = request.get_data()
    # event_str = event.decode("utf-8")

    # return "Hello from SCF Web function, your input: " + event_str + ", request_id: " + request_id + "\n"
    #parallelIndex = 100
    #temp = alu(loopTime, parallelIndex)
    retTime = GetTime()
    return {
        "startTime": startTime,
        "retTime": retTime,
        "execTime": retTime - startTime,
        "result": temp,
    }

##@app.route('/event-invoke', methods = ['POST'])
#def invoke():
 # Get all the HTTP headers from the official documentation of Tencent
 #   request_id = request.headers.get("X-Scf-Request-Id", "")
  #  print("SCF Invoke RequestId: " + request_id)
   # event = {}
    #result = handler(event)
   # print(result)
    #return "1000 size graph BFS finished!" + "计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"

#@app.#route('/web-invoke/python-flask-http', methods = ['POST','GET'])
#def web_invoke():
    # Get all the HTTP headers from the official documentation of Tencent
  #  request_id = request.headers.get("X-Scf-Request-Id", "")
 #   print("SCF Invoke RequestId: " + request_id)
    #event ={}
   # result = handler(event)
   # print(result)
    #return "1000 size graph BFS finished!" + "计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
