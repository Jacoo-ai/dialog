from queue import Queue

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
text_queue = Queue()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_text', methods=['POST', 'GET'])
def send_text():
    data = __request_parse(request)
    text = data.get('text_content')

    text_queue.put(text)
    print(text)
    return "success"


@app.route('/get_text', methods=['GET'])
def get_text():
    if text_queue.empty():
        return jsonify(text_content="")
    return jsonify(text_content=text_queue.get())


initialized = False


@app.route('/web_init', methods=['GET'])
def web_init():
    global initialized
    initialized = True
    return "initialized"


def __request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


class FlaskService:
    def __init__(self):
        app.config['SECRET_KEY'] = os.urandom(24)
        self.initialized = False

    def run(self):
        app.run(debug=False, use_reloader=False)

    def get_initialized(self):
        if initialized:
            self.initialized = True
        return self.initialized


if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=False, use_reloader=False, port=1234)
