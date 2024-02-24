import re
import time

from nltk.tokenize import sent_tokenize

text_stack = []
last_text_content = ""


def push_paragraph(paragraph):
    sentences = sent_tokenize(paragraph)
    while len(sentences) > 0:
        text_stack.append(sentences.pop())


def translate_data_start(flask_state, speed):
    global last_text_content

    while True:
        duration = speed

        if text_stack and flask_state.tts_text_content == "" and flask_state.tts_enable:
            flask_state.tts_text_content = text_stack.pop()
            last_text_content = flask_state.tts_text_content
            duration = len(re.split(r'\s|[,;.]+', flask_state.tts_text_content)) * speed
        time.sleep(duration)


def push_stop_information():
    global last_text_content

    if check_necessary_insert_stop_information():
        push_paragraph(last_text_content)
        push_paragraph("Let's continue our class.")


def check_necessary_insert_stop_information():
    return not ("Let's continue our class." in text_stack)
