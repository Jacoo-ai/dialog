import subprocess
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
            return ""
        return response[0]['text']

    def change_model(self, model_path):
        self.__model_path = model_path
        self.__agent = Agent.load(self.__model_path)

    def wait_for_rasa_text(self, text):
        text = asyncio.run(self.__parse_message(text))
        return text


model_path = "20240309-224423-upbeat-resistivity.tar.gz"
# model_path = "rasa_train/models/20240305-012050-cool-persian.tar.gz"
# model_path = "rasa_train/models/20240213-212046-largo-twitch.tar.gz"
print("rasa server started...")
rasa_service = Rasa(model_path)


# if __name__ == '__main__':
#     model_path = "../../rasa_train/models/20240212-001803-obsolete-rent.tar.gz"
#     rasa_service = Rasa(model_path)
