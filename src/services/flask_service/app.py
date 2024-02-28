import logging
from threading import Condition

from flask import Flask, render_template, request
from flask_socketio import SocketIO
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


class FlaskState:
    def __init__(self):
        self.tts_text_content = ""
        self.asr_text_content = ""
        self.tts_enable = False
        self.condition = Condition()


state = FlaskState()
app = Flask(__name__)
socketio = SocketIO(app)


# Connect
# ==================================================================================
@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/')
def index():
    return render_template('index.html')


# TTS
# ==================================================================================
@app.route('/tts_end', methods=['POST', 'GET'])
def tts_end():
    state.tts_text_content = ""
    state.tts_enable = True
    return ''


@app.route('/tts_start', methods=['POST', 'GET'])
def tts_start():
    state.tts_enable = False
    return ''


def send_tts_text(text):
    state.tts_text_content = text
    socketio.emit('get_tts_text', {'text_content': text})


def send_tts_stop_command():
    socketio.emit('get_tts_command', {'command': "stop"})


# ASR
# ==================================================================================
@app.route('/asr_text', methods=['POST', 'GET'])
def get_text_from_asr():
    data = __request_parse(request)
    state.asr_text_content += data.get('text_content')

    with state.condition:
        state.condition.notify_all()
    return "success"


def wait_for_asr_text_content():
    while state.asr_text_content == "":
        with state.condition:
            state.condition.wait()

    text_content = state.asr_text_content
    state.asr_text_content = ""
    return text_content


# Tools
# ==================================================================================
def __request_parse(req_data):
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def flask_server_start(port=5000):
    print("flask server started at: 127.0.0.1:" + str(port))
    app.config['SECRET_KEY'] = os.urandom(24)
    app.run(debug=False, port=port)


if __name__ == '__main__':
    flask_server_start()
