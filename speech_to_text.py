import speech_recognition as sr
import pyttsx3
import time

# Initialize the recognizer
r = sr.Recognizer()

# Initialize a flag to keep track of whether "bye bye" has been spoken
bye_spoken = False

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def record_text():
    try:
        # Use a microphone as the source of input
        with sr.Microphone() as source2:
            # Wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # Listens for the user's input
            audio2 = r.listen(source2)

            # Using Google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Did you say:", MyText)
            if "goodbye" not in MyText and "bye bye" not in MyText and "bye" not in MyText:
                SpeakText(MyText)
            else:
                global bye_spoken
                if not bye_spoken:
                    SpeakText("Bye Bye")
                    bye_spoken = True
                exit()
            return MyText

    except sr.WaitTimeoutError:
        print("No response received. Speaking 'Bye Bye' and exiting.")
        if not bye_spoken:
            SpeakText("Bye Bye")
            bye_spoken = True
        exit()
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("No speech detected")
        return ""  # Return an empty string in this case

def output_text(text):
    if text:
        f = open("output.txt", "a")
        f.write(text)
        f.write("\n")
        f.close()

while True:
    text = record_text()
    output_text(text)

    if bye_spoken:
        break
