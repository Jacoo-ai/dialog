# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"



# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionRepeatLastBotMessage(Action):
    def name(self) -> str:
        return "action_repeat_last_bot_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        last_bot_message = None
        for event in reversed(tracker.events):
            if event.get("event") == "bot":
                if "text" in event:
                    last_bot_message = event
                    break

        if last_bot_message is not None:
            dispatcher.utter_message(text=last_bot_message["text"])
        else:
            # 如果没有找到机器人的消息，发送一个默认回复
            dispatcher.utter_message(text="I'm not sure how to repeat that, can you ask again?")

        return []
