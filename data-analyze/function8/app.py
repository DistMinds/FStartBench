from flask import Flask, request
import numpy as np
import pandas as pd
from time import time
import json

# 随机生成两个n*n的矩阵，计算相乘的结果，并返回计算时间
def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = (time() - start)*1000
    return latency

app = Flask(__name__)

@app.route('/event-invoke', methods = ['POST'])
def invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)

    event = request.get_data()
    event_str = event.decode("utf-8") 
    n = json.loads(event_str)['n']  # 字符串转字典
    result = matmul(int(n)) 
    print(result)

    return "输入的n为：" + n + "矩阵计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"

@app.route('/web-invoke/python-flask-http', methods = ['POST','GET'])
def web_invoke():
    # Get all the HTTP headers from the official documentation of Tencent
    request_id = request.headers.get("X-Scf-Request-Id", "")
    print("SCF Invoke RequestId: " + request_id)
    
    # 创建dataframe
    df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006], 
 "date":pd.date_range('20130102', periods=6),
  "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
 "age":[23,44,54,32,34,32],
 "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
  "price":[1200,np.nan,2133,5433,np.nan,4432]},
  columns =['id','date','city','category','age','price'])
    print(df)


    event = request.get_data()
    event_str = event.decode("utf-8") 
    n = json.loads(event_str)['n']  # 字符串转字典
    result = matmul(int(n)) 
    print(result)

    return "输入的n为：" + n + "矩阵计算时间为："+str(result)+"ms, request_id: " + request_id + "\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
