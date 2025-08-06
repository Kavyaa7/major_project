import speech_recognition as sr
import pyttsx3
import smtplib
import pyaudio
from email.message import EmailMessage
import time

stt = sr.Recognizer()
#tts = pyttsx3.init(driverName='sapi5')

#voices = tts.getProperty('voices')
#tts.setProperty('voice', voices[1].id) 

HOST = "smtp.gmail.com" 
PORT = 587

from_email = "sampleuser436@gmail.com"
app_password = "hdtq fqgf full zkxo"

def talk(text):
    print("TTS: ",text)
    try:
         tts = pyttsx3.init('sapi5')
         voices = tts.getProperty('voices')
         tts.setProperty('voice', voices[1].id)
         tts.say(text)
         tts.runAndWait()
         tts.stop()
         time.sleep(0.1)
    except Exception as e:
         print("Error in Text-to-Speech: ",e)

def mic(retries=2):
    print("Listening...")
    for attempt in range(retries):
        try:
            talk("Speak now")
            with sr.Microphone() as source:
                stt.adjust_for_ambient_noise(source, duration=1)
                print("Say something...")
                audio = stt.listen(source, timeout=5, phrase_time_limit=5)
                text = stt.recognize_google(audio)
                print("You said:", text)
                return text.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. You didn't speak.")
            talk("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
            talk("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print("Speech Recognition API error:", e)
            talk("There was an error connecting to speech recognition service.")
            break
        except Exception as e:
            print("Unexpected error:", e)
            talk("Unexpected error occurred.")
            break
    return ""  

    
def send_email(receiver,subject,body):
    try:
            server = smtplib.SMTP(HOST,PORT)
            server.ehlo()
            server.starttls()
            server.login(from_email,app_password)
            msg = EmailMessage()
            msg['From'] = from_email
            msg['To'] = receiver
            msg['Subject'] = subject
            msg.set_content(body)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
            talk("Email sent successfully")
    except Exception as e:
        print("An error occurred:", e)
        talk("An error occurred while sending the email")

def main_prog():
     contact_dict = {"kavya": "kavya.s1790@gmail.com"}
     talk("Tell the sender's name")
     name = mic()
     receiver = contact_dict.get(name)
     if receiver is None:
          print("Recipient not found")
          talk("Recipient not found")
          return
     talk("What is the subject of the mail?")
     subject = mic()
     talk("What is the body of the mail?")
     body = mic()
     send_email(receiver,subject,body)

if __name__=="__main__":
     main_prog()

     

