from config import config
from services.rasa_service.rasa import Rasa


def print_text(text):
    print("\n\n\n# ==================================== #")
    print(text)
    print("\n\n\n")


def main():
    model_path = config['rasa']['model_path']
    rasa_service = Rasa(model_path)
    text = rasa_service.wait_for_response("Can you introduce yourself?")
    print_text(text)
    text = rasa_service.wait_for_response("Please begin the lesson.")
    print_text(text)
    text = rasa_service.wait_for_response("Could you clarify at what altitude it's hard to breathe?")
    print_text(text)
    text = rasa_service.wait_for_response("Please continue.")
    print_text(text)
    text = rasa_service.wait_for_response("How long did it take him to climb Everest?")
    print_text(text)
    text = rasa_service.wait_for_response("Please continue.")
    print_text(text)


if __name__ == "__main__":
    main()
