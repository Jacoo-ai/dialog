import sys
import time

import requests
# from app.app import FlaskService
from config import config
from services.rasa_service.rasa import Rasa

# app = FlaskService()
model_path = config['rasa']['model_path']
rasa_service = Rasa(model_path)


def send_text(text):
    json_data = {'text_content': text}  # 要发送的JSON数据
    response = requests.post("http://127.0.0.1:1234/send_text", json=json_data)

    print("\n\n\n# ==================================== #")
    print(text)
    print(response)
    print("\n\n\n")


def slow_print_waiting():
    for i in range(7):  # 8 表示点号的个数
        sys.stdout.write("\rwaiting" + "." * i)
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rwaiting")  # 回到 "waiting"
    sys.stdout.flush()
    time.sleep(1)


def rasa_test():
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
#     app.run()


if __name__ == "__main__":
    # with ProcessPoolExecutor(max_workers=8) as executor:
    #     executor.submit(flask_service)
    #
    # while not app.get_initialized():
    #     slow_print_waiting()

    rasa_test()
    # flask_thread = threading.Thread(target=rasa_test)
    # flask_thread.start()

    # flask_service()
