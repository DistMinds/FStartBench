from textblob import TextBlob
from flask import Flask, request
sentiment_text = "We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.--That to secure these rights, Governments are instituted among Men, deriving their just powers from the consent of the governed, --That whenever any Form of Government becomes destructive of these ends, it is the Right of the People to alter or to abolish it, and to institute new Government, laying its foundation on such principles and organizing its powers in such form, as to them shall seem most likely to effect their Safety and Happiness. Prudence, indeed, will dictate that Governments long established should not be changed for light and transient causes; and accordingly all experience hath shewn, that mankind are more disposed to suffer, while evils are sufferable, than to right themselves by abolishing the forms to which they are accustomed. But when a long train of abuses and usurpations, pursuing invariably the same Object evinces a design to reduce them under absolute Despotism, it is their right, it is their duty, to throw off such Government, and to provide new Guards for their future security.--Such has been the patient sufferance of these Colonies; and such is now the necessity which constrains them to alter their former Systems of Government. The history of the present King of Great Britain is a history of repeated injuries and usurpations, all having in direct object the establishment of an absolute Tyranny over these States. To prove this, let Facts be submitted to a candid world."

def analyze(text):
    analyse = TextBlob(text)
    num_sentences = len(analyse.sentences)
    subjectivity = sum([sentence.sentiment.subjectivity for sentence in analyse.sentences]) / num_sentences
    polarity = sum([sentence.sentiment.polarity for sentence in analyse.sentences]) / num_sentences
    return subjectivity, polarity

def handler(event, context=None):
    subjectivity, polarity = analyze(sentiment_text)

    return {
        "result": "Sentiment analysis finished! Subjectivity {}, Polarity {}.".format(subjectivity, polarity)
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
