import re
import time

from nltk.tokenize import sent_tokenize


class TextState:
    def __init__(self):
        self.text_stack = []
        self.connect_text = "Ok, Let's continue our class."
        self.last_text_content = ""
        self.pop_enable = True
        self.ask_enable = False


state = TextState()


def push_paragraph(paragraph):
    sentences = sent_tokenize(paragraph)
    while len(sentences) > 0:
        state.text_stack.append(sentences.pop())


def push_stop_information():
    if not (state.connect_text in state.text_stack):
        push_paragraph(state.last_text_content)
        push_paragraph(state.connect_text)


def disable_pop():
    state.pop_enable = False


def enable_pop():
    state.pop_enable = True


def extract_text(text):
    pattern = r"@(\w+)\[(.*)\]"

    match = re.search(pattern, text)
    if match:
        command, content = match.groups()
        return content
    else:
        return ""


def judge_format(text, command):
    pattern = r"^@" + re.escape(command) + r"\[.*\]$"

    if re.match(pattern, text, re.DOTALL):
        return True
    else:
        return False


def text_server_start(flask_server):
    while True:
        text_server_flag = state.text_stack and state.pop_enable
        flask_server_flag = flask_server.state.tts_enable and flask_server.state.tts_text_content == ""
        if text_server_flag and flask_server_flag:
            state.last_text_content = state.text_stack.pop()

            if judge_format(state.last_text_content, "ask"):
                state.ask_enable = True
                state.last_text_content = extract_text(state.last_text_content)
            flask_server.send_tts_text(state.last_text_content)
        else:
            time.sleep(0.1)
