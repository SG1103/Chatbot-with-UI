from flask import Flask, request, jsonify
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
            {"role": "system", "content": "You are a helpful assistant and have to answer as fast and concisely as possible within a few sentences."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    return response


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return 'OK', 200

@app.route('/receive', methods=['POST'])
def receive_data():

    data = request.json


#hello my name is Fatima and am the chief future civil servant

#what other events



    print(data)

    user_question = data.get("fm-question", "No question found")

    # Print the user's query
    print("User's Input:", user_question)

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



'''
    response = openAI(user_query)

    print(response)

    respons = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [response]
                }
            }
        ]
    }
'''





if __name__ == '__main__':
    app.run(debug=True, port=5000)
