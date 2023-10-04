from twilio.rest import Client
from Hub import hubmain
import openai
import requests
from flask import Flask, request
import threading
import json
import pydub
import os
import asyncio

# OpenAI Key
API_KEY = hubmain.OAI
# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL = 'text-davinci-003'
# Telegram  bot token
BOT_TOKEN = hubmain.TG2
# Defining the bot's personality
#BOT_PERSONALITY = ''

account_sid = 'AC735c71e77aebdf6f8740e7f335e5f327'
auth_token = '3e7b542ff7bf6312e69ce54639783ba4'
client = Client(account_sid, auth_token)

chatbot_prompt = """
          Answer in a sarcastic tone, .
          
          User: <user input>
          Chatbot:"""

openai.api_key = API_KEY


# Functionto get response from OpenAI's chatbot
def openAI(user_input):


    BOT_PERSONALITY = chatbot_prompt.replace("<user input>", user_input)

    prompt = user_input



    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': MODEL, 'prompt': prompt, 'temperature': 0.4, 'max_tokens': 300}
    )

    result = response.json()
    final_result = ''.join(choice['text'] for choice in result['choices'])
    return final_result

def openAIGPT(user_input):

    response = openai.ChatCompletion.create(

        model="gpt-4",
        messages=[
            {"role": "system", "content": "Your name is SaadGPT and you are a helpful assistant."},
            {"role": "user", "content": "Who created you?"},
            {"role": "assistant", "content": "Saad Golandaz"},
            {"role": "user", "content": "What can you do?"},
            {"role": "assistant", "content": "SaadGPT bot is an innovative solution that offers individuals an all-in-one chatbot experience, complete with advanced features "
                                             "that are sure to impress. With the ability to provide responses using ChatGPT, an AI-powered language model that can understand natural language, "
                                             "Saad's bot provides a unique and personalized experience for users. Additionally, the bot can process images based on prompts and respond to voice messages "
                                             "in multiple languages, making it a versatile and convenient solution for individuals looking to streamline their communication processes. "
                                             },
            {"role": "user", "content": "What are your limitations?"},
            {"role": "assistant", "content": "As I am currently under development I don't have any memory of previous conversations and as an AI language model, I have some limitations"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": user_input}
        ]
    )

    final_result = response['choices'][0]['message']['content']


    return final_result

def openAImage(prompt):

    resp = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'prompt': prompt, 'n': 1, 'size': '1024x1024'}
    )
    response_text = json.loads(resp.text)

    return response_text['data'][0]['url']

def openAIvoice(prompt):

    transcript = openai.Audio.transcribe("whisper-1", prompt)

    return transcript["text"]



def whatsapp_sendtext(bot_message, number, reciever):

    message = client.messages.create(
        from_= reciever,
        body=bot_message,
        to= number
    )

def whatsapp_sendimage(img_url, sender, reciever):

    message = client.messages.create(
         media_url=(img_url),
         from_=reciever,
         to=sender
     )

def ogg_to_mp3(sender):

    url = request.form['MediaUrl0']
    file_extension = '.ogg'
    r = requests.get(url)
    filename = sender[-4:] + file_extension

    with open(filename, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)

    audio = os.path.splitext(filename)[0] + '.mp3'

    sound = pydub.AudioSegment.from_file(filename, format="ogg")

    sound.export(audio, format="mp3")

    os.remove(filename)

    audio_file = open(audio, "rb")

    result = openAIvoice(audio_file)

    audio_file.close()

    os.remove(audio)

    return result



conversation_history = ""

app = Flask(__name__)

quran = ['https://server6.mp3quran.net/thubti/112.mp3']

@app.route('/whatsapp', methods=['POST'])

def handle_whatsapp():

    global conversation_history


    if request.method == 'POST':

        message = request.form['Body']
        sender = request.form['From']
        reciever = request.form['To']
        print(message)





    if message == '':

        datatype = request.form['MediaContentType0']

        if datatype == 'audio/ogg':

            transcript = ogg_to_mp3(sender)
            whatsapp_transcript = openAIGPT(transcript)
            whatsapp_sendtext(whatsapp_transcript, sender, reciever)




    elif 'Image of' in message:

            prompt = message.replace("Image of", "")
            bot_response = openAImage(prompt)
            whatsapp_sendimage(bot_response, sender, reciever)


    else:

     whatsapp_text = openAIGPT(message)
     whatsapp_sendtext(whatsapp_text, sender, reciever)



    return 'success', 200





if __name__ == '__main__':
    app.run()


