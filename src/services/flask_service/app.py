import logging
from queue import Queue
from threading import Condition

from flask import Flask, render_template, request, jsonify
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask(__name__)
text_queue = Queue()
tts_enable = False
asr_enable = False

condition = Condition()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_text', methods=['POST', 'GET'])
def send_text():
    data = __request_parse(request)
    text = data.get('text_content')

    text_queue.put(text)
    return "success"


@app.route('/get_text', methods=['GET'])
def get_text():
    if text_queue.empty() or not tts_enable:
        return jsonify(text_content="")
    return jsonify(text_content=text_queue.get())


@app.route('/enable_tts', methods=['GET'])
def enable_tts():
    global tts_enable

    tts_enable = True
    with condition:
        condition.notify_all()
    return "tts_enabled"


@app.route('/disable_tts', methods=['GET'])
def disable_tts():
    global tts_enable

    tts_enable = False
    with condition:
        condition.notify_all()
    return "tts_disabled"


@app.route('/tts_end', methods=['GET'])
def enable_asr():
    global asr_enable

    asr_enable = True
    with condition:
        condition.notify_all()
    return 'asr_enabled'


@app.route('/tts_start', methods=['GET'])
def disable_asr():
    global asr_enable

    asr_enable = False
    with condition:
        condition.notify_all()
    return 'asr_disabled'


def __request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def flask_server_start(port=5000):
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=False, port=port)
    print("flask server started at: 127.0.0.1:" + str(port) + "...")


def get_speak_state():
    return asr_enable and tts_enable


def get_speak_start_state():
    return not asr_enable
    # return True if not asr_enable else False


if __name__ == '__main__':
    flask_server_start()
