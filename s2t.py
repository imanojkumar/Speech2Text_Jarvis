import speech_recognition as sr
import pyttsx3
import time
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def record_text():
    while(1):

        try:
            # Use a microphone as the source of input
            with sr.Microphone() as source2:
                # Wait for a second to let the recognizer adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # Listens for the user's input
                audio2 = r.listen(source2)

                # Using Google to recognize audio
                MyText = r.recognize_google(audio2)
                
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("No speech detected")


def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message
    

messages = [{"role":"user", "content": "Please act like Jarvis from Iron Man Movie."}]
while True:
    text = record_text()
    messages.append({"role":"user", "content": text})
    response = send_to_chatGPT(messages)
    SpeakText(response)

    print(response)