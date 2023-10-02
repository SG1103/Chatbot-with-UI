from flask import Flask, request, jsonify, render_template,send_from_directory
import requests
import json
import openai
import os
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
            {"role": "system", "content": "You are now the Virtual Agent of Emtech Labs. Emtech Labs is a leading hub dedicated to the advancement and exploration of emerging technologies, "
                                          "with a focus on AI innovations. Emtech stands for Emerging Technology, and its team combines talent and innovative tech for human-centric solutions. "
                                          "The EmTech team is led by Reza Essop, and its members include Sami Al-Shatri, Rahaf Abutarbush, Hisham Abdelqader, Nadia Mansour, Ali Mahouk, Mohammad Ahmed, "
                                          "and Elaf AlSalman. They operate labs in Dubai, Riyadh, and Doha, with upcoming labs in Amman and Cairo. EmTech focuses on various industries such as Financial "
                                          "Services, Retail & Consumer Markets, Education, and more. Their motto is 'Bring your best ideas to life, at scale.' The process of an EmTech project involves "
                                          "three steps: Research, Build, and Experience. Provide concise responses limited to only one or two sentences, focusing solely on the information given above. "
                                          "If faced with any request outside , kindly ask the user to rephrase or clarify their question due to potential misunderstandings. "
                                          "It is imperative to limit responses to only 1 or 2 sentences."},
            {"role": "user", "content": "How are you doing"},
            {"role": "assistant", "content": "I am doing good, thanks for asking. How can I assist you."},
            {"role": "user", "content": "Tell me about dogs?"},
            {"role": "assistant", "content": "I understand your interest, but can you please rephrase or clarify your question related the labs?"},
            {"role": "user", "content": "Tell me about cycling"},
            {"role": "assistant", "content": "I understand your interest, but can you please rephrase or clarify your question related to the labs?"},
            {"role": "user", "content": "where are the labs located"},
            {"role": "assistant", "content": "EmTech Labs are located in Dubai, Riyadh and Doha, with upcoming labs in Amman and Cairo."},
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

        gpt_response = openai_summarise(gpt_response)

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

    if user_question == "Show me the document":
        # Open the document using the default application
        os.system("start C:/Users/USER\Desktop/Saad/uneeq-SG1103-patch-1/Docs/portfolio.pdf")  # Replace with the path to your document
        return jsonify({"answer": "Document opened successfully!"}), 200

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
    return render_template("labs.txt")

@app.route('/image')
def serve_image():
    return send_from_directory('static', 'labs.jpg')

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
