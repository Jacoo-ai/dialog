import re
from threading import Thread

from services.flask_service import app as flask_server
from services.rasa_service.rasa_service import rasa_service as rasa_server
import src.services.text_service.text_service as text_server


def wait_story_continue():
    while True:
        asr_text_content = flask_server.wait_for_asr_text_content()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        if text_server.judge_format(rasa_text_content, "story_continue"):
            extract_text_content = text_server.extract_text(rasa_text_content)
            text_server.push_paragraph(extract_text_content)
            break
    text_server.state.ask_enable = False


def ask_and_response():
    while True:
        asr_text_content = flask_server.wait_for_asr_text_content()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        if text_server.judge_format(rasa_text_content, "continue"):
            break

        if text_server.judge_format(rasa_text_content, "answer"):
            extract_text_content = text_server.extract_text(rasa_text_content)
            flask_server.send_tts_text(extract_text_content)


def interrupt():
    text_server.disable_pop()

    flask_server.send_tts_text("Ok, What's your questions?")
    text_server.push_stop_information()
    flask_server.send_tts_stop_command()

    ask_and_response()

    text_server.enable_pop()


def process_sentences():
    while True:
        asr_text_content = flask_server.wait_for_asr_text_content()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        print("==========================================================================================")
        print(asr_text_content)
        print(rasa_text_content)
        print()

        if (text_server.judge_format(rasa_text_content, "stop")) and (not flask_server.state.tts_enable):
            interrupt()
        elif text_server.state.ask_enable:
            wait_story_continue()
        elif not flask_server.state.tts_enable:
            continue
        elif text_server.judge_format(rasa_text_content, "story") or text_server.judge_format(rasa_text_content,
                                                                                              "answer"):
            extract_text_content = text_server.extract_text(rasa_text_content)
            text_server.push_paragraph(extract_text_content)


def run_text_server():
    text_server.text_server_start(flask_server)


def run_flask_server():
    flask_server.flask_server_start(port=5000)


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_server)
    process_sentences_thread = Thread(target=process_sentences)
    text_thread = Thread(target=run_text_server)

    flask_thread.start()
    process_sentences_thread.start()
    text_thread.start()

    process_sentences_thread.join()
    flask_thread.join()
    text_thread.join()
