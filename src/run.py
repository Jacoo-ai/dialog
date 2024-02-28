from threading import Thread

from services.flask_service import app as flask_server
from services.rasa_service.rasa_service import rasa_service as rasa_server
import src.services.text_service.text_service as text_server


def debug_text():
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print(text_server.state.text_stack)
    # print(text_server.state.last_text_content)
    # print(text_server.state.pop_enable)
    #
    # print(flask_server.state.asr_text_content)
    # print(flask_server.state.tts_text_content)
    # print(flask_server.state.tts_enable)
    # print()
    pass


def process_sentences():
    while True:
        debug_text()
        asr_text_content = flask_server.wait_for_asr_text_content()

        if ("stop" in asr_text_content.lower()) and (not flask_server.state.tts_enable):
            text_server.disable_pop()

            flask_server.send_tts_text("Ok, What's your questions?")
            text_server.push_stop_information()
            flask_server.send_tts_stop_command()

            asr_text_content = flask_server.wait_for_asr_text_content()
            rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
            text_server.push_paragraph(rasa_text_content)
            text_server.enable_pop()
            continue
        elif not flask_server.state.tts_enable:
            continue

        print("==========================================================================================")
        print(asr_text_content)
        print()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        text_server.push_paragraph(rasa_text_content)


def run_text_server():
    text_server.text_server_start(flask_server)


def run_flask_server():
    flask_server.flask_server_start(port=5000)


def run_rasa_action_server():
    rasa_server.rasa_actions_start()


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_server)
    rasa_action_thread = Thread(target=run_rasa_action_server)
    process_sentences_thread = Thread(target=process_sentences)
    text_thread = Thread(target=run_text_server)

    rasa_action_thread.start()
    flask_thread.start()
    process_sentences_thread.start()
    text_thread.start()

    process_sentences_thread.join()
    rasa_action_thread.join()
    flask_thread.join()
    text_thread.join()
