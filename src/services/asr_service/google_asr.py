import speech_recognition as sr

import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "services/asr_service/resources/elite-matter-414516-4e3716bbce5e.json"
recognizer = sr.Recognizer()


def record_audio(duration=5, sample_rate=44100, channels=1):
    """record the audio of the user's speech from Microphone"""

    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
    return audio


def record_and_recognize(duration=5):
    audio_data = record_audio()
    """using speech_recognition api to recognize speech from the user"""

    print('recognizing')
    try:
        # text = recognizer.recognize_google_cloud(audio_data=audio_data)
        text = recognizer.recognize_google(audio_data)
        print("you said: " + text)
        return text
    except sr.UnknownValueError:
        return 'could not understand'
    except sr.RequestError as e:
        return 'could not request results from google' + str(e)


if __name__ == '__main__':
    result = record_and_recognize()
    print(result)
