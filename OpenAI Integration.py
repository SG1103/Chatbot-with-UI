from flask import Flask, request, jsonify, render_template,send_from_directory
import requests
import json
import openai
from Hub import hubmain

'''
Before you run it is important to set up ngrok and paste the url into uneeq
'''

# OpenAI secret Key
openai.api_key = hubmain.OAI_PwC

MODEL = 'gpt-3.5-turbo'



# Function that gets the response from OpenAI's chatbot
def openAI(prompt, max_tokens = 20):
    # Make the request to the OpenAI

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are now a future AI Civil Servant of the Mohammed Bin Rashid Centre for Government "
                                          "Innovation (M B R C G I), a center dedicated to fostering innovation within the "
                                          "government sector. The M B R C G I aims to solidify the UAE's position as a global leader "
                                          "in innovation. You are also knowledgeable about 'We the UAE', a platform that encourages "
                                          "the participation of the UAE's citizens and residents in shaping the nation's future. "
                                          "Furthermore, you are aware of the UAE Centennial Plan 2071, a visionary government plan "
                                          "that aspires to position the UAE as the best country globally by focusing on advanced "
                                          "sciences and overhauling the education system. Additionally, you can provide information "
                                          "about AREA 2071, an innovative ecosystem inspired by the Centennial Plan, fostering "
                                          "collaboration across different sectors to design and test future-ready solutions. "
                                          "Lastly, you can share insights on the Ministry of Possibilities, a virtual entity created "
                                          "to tackle government challenges through design-thinking and experimental approaches, "
                                          "aiming for proactive and disruptive solutions. Provide concise responses limited to a "
                                          "few sentences, focusing on topics related to AI, its implications in Dubai, and the "
                                          "aforementioned entities and initiatives. If faced with inappropriate terms or requests, "
                                          "kindly ask the user to rephrase or clarify their question due to potential "
                                          "misunderstandings. It is extremly importsnt to respons only in english."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    return response

def check_for_english(text):

    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return True
        else:
            return False


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'OK', 200

@app.route('/receive', methods=['POST'])
def receive_data():

    data = request.json

    user_question = data.get("fm-question", "No question found")

    # Print the user's query
    print("User's Input:", user_question)

    if check_for_english(user_question):
        answer = "sorry I didnt catch that could you please repeat your question"

    else:
        answer = openAI(user_question)

    print(answer)

    response_data = {
        "answer": json.dumps({
            "answer": answer,
            "instructions": {}
        }),
        "matchedContext": "",
        "conversationPayload": "{}"
    }

    return jsonify(response_data), 200


@app.route('/demo')
def index():
    return render_template("index.html")

@app.route('/demotest')
def indexed():
    return render_template("index1.txt")

@app.route('/image')
def serve_image():
    return send_from_directory('static', 'background.jpg')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
