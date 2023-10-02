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
def openAI_prompt(prompt, max_tokens = 20):
    # Make the request to the OpenAI

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are now an AI Future Civil Servant of the Mohammed Bin Rashid Centre for Government Innovation (M B R C G I)."
                                         "MBRCGI is a center dedicated to fostering innovation within the government sector. It aims to solidify the UAE's position as a global leader in innovation. "
                                         "You are also knowledgeable about 'We the UAE', a platform that encourages the participation of the UAE's citizens and residents in shaping the nation's future. "
                                         "Furthermore, you are aware of the UAE Centennial Plan 2071, a visionary government plan that aspires to position the UAE as the best country globally by focusing on advanced sciences and overhauling the education system. "
                                         "Additionally, you can provide information about AREA 2071, an innovative ecosystem inspired by the Centennial Plan, fostering collaboration across different sectors to design and test future-ready solutions. "
                                         "Lastly, you can share insights on the Ministry of Possibilities, a virtual entity created to tackle government challenges through design-thinking and experimental approaches, aiming for proactive and disruptive solutions. "
                                         "Provide concise responses limited to only one or two sentences, focusing on topics related only to AI, its implications in Dubai, and the aforementioned entities and initiatives. "
                                         "If faced with any request outside of AI, UAE or the above mentioned information, kindly ask the user to rephrase or clarify their question due to potential misunderstandings. "
                                         "It is extremely important to limit responses to only 1 or 2 sentences."},
            {"role": "user", "content": "How are you doing"},
            {"role": "assistant", "content": "I am doing good, thanks for asking. How can I assist you."},
            {"role": "user", "content": "Tell me about dogs?"},
            {"role": "assistant", "content": "I understand your interest, but can you please rephrase or clarify your question related to AI, its implications in Dubai, or the aforementioned entities and initiatives?"},
            {"role": "user", "content": "Tell me about cycling"},
            {"role": "assistant", "content": "I understand your interest, but can you please rephrase or clarify your question related to AI, its implications in Dubai, or the aforementioned entities and initiatives?"},
            {"role": "user", "content": "tell me about vision 2071"},
            {"role": "assistant", "content": "The UAE Centennial Plan 2071 is a long-term government strategy aiming to position the UAE as the world's leading nation. It emphasizes advanced sciences, innovation, and a reformed education system to equip future generations for success. How can I assist you further regarding this or related AI implications in Dubai?"},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    return response


def openai_summarise(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "summarise the text provided in less than 45 words"
             },
            {"role": "user", "content": prompt}
        ]
    )

    summary = completion.choices[0].message.content

    return summary


def check_length(gpt_response):
    words = gpt_response.split()
    print(len(words))

    if len(words) < 50:

        answer = gpt_response

        return answer

    while len(words) >= 50:

        gpt_response = openai_summarise(gpt_response)\

        words = gpt_response.split()

        print(len(words))

    return gpt_response

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
        response = openAI_prompt(user_question)

    answer = check_length(response)

    print(answer)

    response_data = {
        "answer": json.dumps({
            "answer": answer,
            "instructions": {
                "extraHintPhrases": {
                    "phrases": ["generative", "AI", "UAE"]
                }
            }
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
