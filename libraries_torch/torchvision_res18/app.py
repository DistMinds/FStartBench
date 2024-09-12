import io
import os
import sys
import json
import torch
from torchvision import transforms
from torchvision.models import alexnet
from PIL import Image
from flask import Flask, request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

image_name = "tesla.jpg"
image_url = "https://github.com/spcl/serverless-benchmarks-data/blob/6a17a460f289e166abb47ea6298fb939e80e8beb/400.inference/411.image-recognition/fake-resnet/800px-20180630_Tesla_Model_S_70D_2015_midnight_blue_left_front.jpg?raw=true"
model_name = "resnet18.pth"
model_url = "https://github.com/spcl/serverless-benchmarks-data/blob/6a17a460f289e166abb47ea6298fb939e80e8beb/400.inference/411.image-recognition/model/resnet50-19c8e357.pth?raw=true"
dataset_name = "imagenet_class_index.json"
dataset_url = "https://github.com/spcl/serverless-benchmarks/blob/master/benchmarks/400.inference/411.image-recognition/python/imagenet_class_index.json?raw=true"
local_path = "./"

model = None


def download(url, local_path, filename):
    if not os.path.isfile(local_path + filename):
        with open(local_path + filename, "wb") as f:
            f.write(requests.get(url).content)

def handler(event, context=None):
    # Download dataset
    download(dataset_url, local_path, dataset_name)
    class_idx = json.load(open(os.path.join(local_path, dataset_name), 'r'))
    idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]
    
    # Download image
    download(image_url, local_path, image_name)

    global model
    if not model:
        # Download model checkpoint
        download(model_url, local_path, model_name)
        model = models.resnet18(pretrained=True)
        model.load_state_dict(torch.load(local_path + model_name))
        model.eval()
   
    input_image = Image.open(local_path + image_name)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model 

    output = model(input_batch)
    _, index = torch.max(output, 1)
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    prob = torch.nn.functional.softmax(output[0], dim=0)
    _, indices = torch.sort(output, descending=True)
    ret = idx2label[index]
    results = "Prediction: index {}, class {}".format(index.item(), ret)

    return {
        "result": results
    }


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