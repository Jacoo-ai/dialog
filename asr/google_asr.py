import speech_recognition as sr


def record_audio(duration=5, sample_rate=44100, channels=1):
    """record the audio of the user's speech from Microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    return audio


def recognize_speech(audio_data):
    """using speech_recognition api to recognize speech from the user"""

    recognizer = sr.Recognizer()
    print('recognizing')
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return 'could not understand'
    except sr.RequestError as e:
        return 'could not request results from google'


if __name__ == '__main__':
    audio_data = record_audio()
    result = recognize_speech(audio_data)
    print(result)
