import re
import time

from nltk.tokenize import sent_tokenize

text_stack = []
prompt_text = "Ok, What's your questions?"
connect_text = "Let's continue our class."

def push_paragraph(paragraph):
    sentences = sent_tokenize(paragraph)
    while len(sentences) > 0:
        text_stack.append(sentences.pop())


def translate_data_start(flask_state, speed):
    while True:
        duration = speed

        if text_stack and flask_state.tts_text_content == "" and flask_state.tts_enable:
            flask_state.tts_text_content = text_stack.pop()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(flask_state.tts_text_content)
            print()
            duration = len(re.split(r'\s|[,;.]+', flask_state.tts_text_content)) * speed
        time.sleep(duration)


def push_stop_information():
    if check_necessary_insert_stop_information():
        push_paragraph(connect_text)
        # push_paragraph(prompt_text)


def check_necessary_insert_stop_information():
    return not ("Let's continue our class." in text_stack)
