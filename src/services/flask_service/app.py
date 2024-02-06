from queue import Queue

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
text_queue = Queue()
speak_enable = False


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
    if text_queue.empty() or not speak_enable:
        return jsonify(text_content="")
    return jsonify(text_content=text_queue.get())


@app.route('/enable_speak', methods=['GET'])
def enable_speak():
    global speak_enable

    speak_enable = True
    return "enabled"


@app.route('/disable_speak', methods=['GET'])
def disable_speak():
    global speak_enable

    speak_enable = False
    return "disabled"


@app.route('/get_state', methods=['GET'])
def get_state():
    return "True" if speak_enable else "False"


def __request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def flask_server_start(port=5000):
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=False, use_reloader=False, port=port)

if __name__ == '__main__':

    flask_server_start()
