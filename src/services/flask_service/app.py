import logging
from threading import Condition

from flask import Flask, render_template, request, jsonify
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


class FlaskState:
    def __init__(self):
        self.tts_text_content = ""
        self.asr_text_content = ""
        self.command = ""
        self.tts_enable = False
        self.condition = Condition()


state = FlaskState()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_information', methods=['POST', 'GET'])
def get_information():
    command_str = state.command
    state.command = ""
    if state.tts_text_content != "" and state.tts_enable:
        disable_tts()
        return jsonify(text_content=state.tts_text_content, command=command_str)

    return jsonify(text_content="", command=command_str)


@app.route('/tts_end', methods=['POST', 'GET'])
def enable_tts():
    state.tts_enable = True
    state.tts_text_content = ""

    return 'asr_enabled'


@app.route('/tts_start', methods=['POST', 'GET'])
def disable_tts():
    state.tts_enable = False

    return 'asr_disabled'


@app.route('/asr_text', methods=['POST', 'GET'])
def get_text_from_asr():
    data = __request_parse(request)
    state.asr_text_content = data.get('text_content')

    with state.condition:
        state.condition.notify_all()
    return "success"


def stop_tts():
    state.command = "stop"


def __request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def flask_server_start(port=5000):
    print("flask server started at: 127.0.0.1:" + str(port) + "...")
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=False, port=port)


def wait_for_asr_text():
    with state.condition:
        if state.asr_text_content == "":
            state.condition.wait()
    text_content = state.asr_text_content
    state.asr_text_content = ""
    return text_content


if __name__ == '__main__':
    flask_server_start()
