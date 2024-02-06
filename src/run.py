import sys
import time
from threading import Thread

import requests
from services.flask_service import app as flask_server
from services.rasa_service.rasa import Rasa


def send_text(text):
    json_data = {'text_content': text}  # 要发送的JSON数据
    response = requests.post("http://127.0.0.1:5000/send_text", json=json_data)

    print("\n\n\n# ==================================== #")
    print(text)
    print(response)
    print("\n\n\n")

def wait_speak_enable():
    # print(requests.get("http://127.0.0.1:5000/get_state"))
    while requests.get("http://127.0.0.1:5000/get_state").text != "True":
        time.sleep(0.5)


def slow_print_waiting():
    for i in range(7):  # 8 表示点号的个数
        sys.stdout.write("\rwaiting" + "." * i)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rwaiting")  # 回到 "waiting"
    sys.stdout.flush()
    time.sleep(1)


def rasa_story_1():
    model_path = "rasa_train/models/20240201-235608-cloudy-kern.tar.gz"
    rasa_service = Rasa(model_path)

    wait_speak_enable()
    text = rasa_service.wait_for_response("Can you introduce yourself?")
    send_text(text)
    text = rasa_service.wait_for_response("Please begin the lesson.")
    send_text(text)
    text = rasa_service.wait_for_response("Could you clarify at what altitude it's hard to breathe?")
    send_text(text)
    text = rasa_service.wait_for_response("Please continue.")
    send_text(text)
    text = rasa_service.wait_for_response("How long did it take him to climb Everest?")
    send_text(text)
    text = rasa_service.wait_for_response("Please continue.")
    send_text(text)


# def flask_service():
#     flask_service.run()
def run_flask():
    flask_server.flask_server_start(port=5000)


def run_rasa():
    rasa_story_1()


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    rasa_thread = Thread(target=run_rasa)

    flask_thread.start()
    rasa_thread.start()

    rasa_thread.join()
    flask_thread.join()

