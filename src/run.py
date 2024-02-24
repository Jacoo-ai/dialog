from threading import Thread

from services.flask_service import app as flask_server
from services.rasa_service.rasa_service import rasa_service as rasa_server
import services.text_service.text_service as text_server


def process_sentences():
    is_stop = False
    stop_state = False

    while True:
        asr_text_content = flask_server.wait_for_asr_text()
        rasa_text_content = rasa_server.wait_for_rasa_text(asr_text_content)
        print("==========================================================================================   1")
        print(asr_text_content)
        print()
        if stop_state or (not flask_server.state.tts_enable):
            # disable for inserting new answer into tts_text_content
            flask_server.disable_tts()
            flask_server.stop_tts()
            text_server.push_stop_information()
            is_stop = True

        # 非询问打断，后续直接退出打断状态
        if "stop" in asr_text_content.lower(): # 这句话替换为rasa对于intent: stop的输出
            flask_server.state.tts_text_content = "Ok, What's your questions?"
            stop_state = False

        # 插入回答语句
        text_server.push_paragraph(rasa_text_content)

        # recover tts_enable from breakpoint
        if is_stop:
            flask_server.enable_tts()
            is_stop = False





def run_text_server():
    text_server.translate_data_start(flask_server.state, 0.32)


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
