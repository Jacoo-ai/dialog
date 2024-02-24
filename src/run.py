import time
from threading import Thread

from services.flask_service import app as flask_server
from services.rasa_service.rasa_service import rasa_service as rasa_server
import services.text_service.text_service as text_server


def process_sentences():
    while True:
        asr_text_content = flask_server.wait_for_asr_text()

        if ("stop" in asr_text_content.lower()) and (not flask_server.state.tts_enable):
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(text_server.text_stack)
            print(flask_server.state.tts_text_content)
            print(flask_server.state.tts_enable)
            print()

            # restore and prompt
            flask_server.set_tts_enable(False)
            flask_server.stop_tts()
            time.sleep(10)
            text_server.push_paragraph(flask_server.state.tts_text_content)
            text_server.push_stop_information()
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(text_server.text_stack)
            print(flask_server.state.tts_text_content)
            print(flask_server.state.tts_enable)
            print()

            asr_text_content = flask_server.wait_for_asr_text()
            rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
            text_server.push_paragraph(rasa_text_content)

            flask_server.set_tts_enable(True)
            continue
        elif not flask_server.state.tts_enable:
            continue

        print("==========================================================================================")
        print(asr_text_content)
        print()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        text_server.push_paragraph(rasa_text_content)


def run_text_server():
    text_server.translate_data_start(flask_server.state, 0.3)


def run_flask_server():
    flask_server.flask_server_start(port=5000)


def run_rasa_action_server():
    rasa_server.start_rasa_actions()


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_server)
    rasa_action_thread = Thread(target=run_rasa_action_server)
    process_sentences_thread = Thread(target=process_sentences)
    text_server_thread = Thread(target=run_text_server)

    rasa_action_thread.start()
    flask_thread.start()
    process_sentences_thread.start()
    text_server_thread.start()

    process_sentences_thread.join()
    rasa_action_thread.join()
    flask_thread.join()
    text_server_thread.join()
