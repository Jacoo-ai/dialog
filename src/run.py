from threading import Thread

import requests
from services.flask_service import app as flask_server
from services.rasa_service.rasa_service import rasa_service as rasa_server
from services.asr_service import google_asr as asr_server


def send_text(text):
    json_data = {'text_content': text}
    response = requests.post("http://127.0.0.1:5000/send_text", json=json_data)

    print("# ==================================== #")
    print(text)
    print()


def enable_speak():
    requests.get("http://127.0.0.1:5000/enable_speak")
    print("speak enabled")


def disable_speak():
    requests.get("http://127.0.0.1:5000/disable_speak")
    print("speak enabled")


def wait_speak_enable():
    with flask_server.condition:
        while not flask_server.get_speak_state():
            flask_server.condition.wait()
    # while not flask_server.get_speak_state():
    #     pass


def wait_speak_start():
    with flask_server.condition:
        while not flask_server.get_speak_start_state():
            flask_server.condition.wait()
    # while not flask_server.get_speak_start_state():
    #     pass


def ask_and_response():
    wait_speak_enable()
    user_text = asr_server.record_and_recognize()
    # user_text = input("input request")

    read_text = rasa_server.wait_for_response(user_text)
    send_text(read_text)
    wait_speak_start()
    # time.sleep(5)


def rasa_story_1():
    """
        > Can you introduce yourself?
        > Please begin the lesson.
        > Could you clarify at what altitude it's hard to breathe?
        > Please continue.
        > How long did it take him to climb Everest?
        > Please continue.
    """
    while True:
        ask_and_response()
    # ask_and_response("Can you introduce yourself")
    # ask_and_response("Please begin the lesson")
    # ask_and_response("Could you clarify at what altitude it's hard to breathe")
    # ask_and_response("Please continue")
    # ask_and_response("How long did it take him to climb Everest")
    # ask_and_response("Please continue")


def run_flask():
    flask_server.flask_server_start(port=5000)


def run_rasa():
    rasa_story_1()


def run_rasa_action_server():
    rasa_server.start_rasa_actions()


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    rasa_action_thread = Thread(target=run_rasa_action_server())
    rasa_thread = Thread(target=run_rasa)

    flask_thread.start()
    rasa_action_thread.start()
    rasa_thread.start()

    rasa_thread.join()
    rasa_action_thread.join()
    flask_thread.join()
