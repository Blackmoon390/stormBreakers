from cycler import V
import google.generativeai as genai
import pyttsx3
import os

from regex import V0
genai.configure(api_key="AIzaSyCUgs3Ta_M2kHOrTXr3p8p0S20z7-9Ez-8")

engine=pyttsx3.init()


def content_model(text):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(text)
    responses=response.candidates[0].content.parts[0].text
    print(responses)
    return responses

def text_to_speech(response_text,num):
    if num is None:
        num = 1
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[num].id)
    full_path = r'C:\python\RIT_HACKATHON\static\audio\story5.wav'
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    engine.save_to_file(response_text, full_path)
    engine.runAndWait()

def Voice_Generator(text,num):
    Generated=content_model(text)
    text_to_speech(Generated,num)