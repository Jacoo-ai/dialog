import subprocess
import time
from rasa.model import get_local_model
from rasa.core.agent import Agent

import asyncio


class Rasa:
    def __init__(self, file_path):
        self.__model_path = get_local_model(file_path)
        self.__agent = Agent.load(self.__model_path)

    async def __parse_message(self, text):
        response = await self.__agent.handle_text(text)
        if len(response) == 0:
            return "No response got from rasa"
        return response[0]['text']

    def change_model(self, model_path):
        self.__model_path = model_path
        self.__agent = Agent.load(self.__model_path)

    def wait_for_response(self, text):
        start_time = time.time()
        text = asyncio.run(self.__parse_message(text))
        while text == "" or time.time() - start_time < 5:
            pass
        return text

    @staticmethod
    def start_rasa_actions():
        try:
            subprocess.Popen(["rasa", "run", "actions"], cwd="rasa_train")
            print("动作服务器已启动...")
        except Exception as e:
            print(f"启动动作服务器时出错: {e}")


model_path = "rasa_train/models/20240213-222529-wan-food.tar.gz"
rasa_service = Rasa(model_path)

# if __name__ == '__main__':
#     model_path = "../../rasa_train/models/20240212-001803-obsolete-rent.tar.gz"
#     rasa_service = Rasa(model_path)