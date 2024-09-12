import datetime
import io
import os
import shutil
import uuid
import zlib
from flask import Flask, request
folder_name = "acmart-master"
local_path = "./"

def compress(path, key):
    shutil.make_archive(os.path.join(path, key), 'zip', root_dir=path)
    archive_name = '{}.zip'.format(key)
    archive_size = os.path.getsize(os.path.join(path, archive_name))

    return archive_name, archive_size

def handler(event, context=None):
    archive_name, archive_size = compress(local_path, folder_name)

    return {
        "result": "{} compression in size {} finished!".format(archive_name, archive_size)
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
        "result": temp,
    }
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)

