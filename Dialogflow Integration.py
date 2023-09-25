from flask import Flask, request, jsonify
import requests
import openai
from Hub import hubmain
import time

'''
Before you run it is important to set up ngrok and paste the url into 
googledialogflow es fulfuilment the present code doesn't provide a voice response to uneeq
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
            {"role": "system", "content": "You are a helpful assistant and have to answer as fast and concisely as possible within one or two sentences."},
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

    req_data = request.get_json()

    # Get the user's query from the request data
    user_query = req_data.get('queryResult', {}).get('queryText', '')

    # Print the user's query
    print("User's Input:", user_query)

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

    return jsonify(respons)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
