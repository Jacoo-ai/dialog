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
