from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
from unidecode import unidecode
import pandas as pd
import re


app = Flask(__name__) #deklarasi Flask
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API for text cleansing'),
    'version': LazyString(lambda: '1'),
    'description': LazyString(lambda: 'An API that helps clean your text from emojis, punctuation, new lines, and bytes'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

def newline_removal(s):
    s = s.strip().replace(r"\n"," ")
    return s

def ascii_removal1(s):
    s = s.encode().decode('unidecode_escape')
    s = bytes('latin-1').decode('utf-8')
    return s
def ascii_removal2(s):
    return re.sub(r"\\x[A-Za-z0-9./]+", '', unidecode(s))

def remove_emojis(s):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', s)

def punc_removal(s):
    return re.sub(r"[^\w\d\s]", "", s)

@swag_from("swagger_config_post.yml", methods=['POST'])
@app.route("/text_cleaning/v1", methods=["POST"])
def text_cleaning():
    s = request.get_json()
    s = s['Text']
    s = s.strip()
    s = s.replace(r"\n"," ")
    s = bytes(s, 'utf-8').decode('utf-8', 'ignore')
    s = punc_removal(s)
    return jsonify({"cleaned text":cleanedtext})

if __name__ == "__main__":
    app.run(port=1235, debug=True)
