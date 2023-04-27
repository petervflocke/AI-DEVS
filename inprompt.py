import requests
import sys
import os
import json
import logging
import openai

def chat_completion(input_text, question_text):
    system_text = "### BAZADANYCH" + "\n" + input_text +"/BAZADANYCH" + "\n"
    question_text = 'Use BAZADANYCH to answer this question:' + question_text + \
                'Answer in following JSON format {"output": answer}. If there is no such a person return only one word "BAZINGA"'

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant.\n" + system_text},
            {"role": "user", "content": question_text}
        ]
)

    message = response['choices'][0]['message']['content']
    return message


if len(sys.argv) > 1:
    DEBUG_MODE=sys.argv[1]
else:
    #DEBUG_MODE = "debug", "info", anything else for off
    DEBUG_MODE="off"
if DEBUG_MODE == "debug":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
elif DEBUG_MODE == "info":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.disable(sys.maxsize)

TASKNAME = os.path.splitext(os.path.basename(__file__))[0]
logging.info(f"Task name: {TASKNAME}")

KEY = os.environ.get('AIDEVS')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

URL_AI_DEVS = os.environ.get('URL_AI_DEVS')
TOKEN = "/token/"
TASK = "/task/"
ANSWER = "/answer/"

if not KEY:
    raise ValueError("API KEY cannot be empty, setup environment variable AIDEVS")
if not OPENAI_API_KEY:
    raise ValueError("openAI API KEY cannot be empty, setup environment variable OPENAI_API_KEY")
if not URL_AI_DEVS:
    raise ValueError("URL for AI_devs cannot be empty, setup environment variable URLAIDEVS")

logging.debug(f"Key: {KEY}; TaskName:{TASKNAME}")

data = {
    "apikey": f"{KEY}",
}

response = requests.post(URL_AI_DEVS+TOKEN+TASKNAME, json=data)
json_response = response.json()
logging.info(f"Received json: {json_response}")
token = json_response.get("token")

response = requests.get(URL_AI_DEVS+TASK+token)
json_response = response.json()
logging.info(f"Received json: {json_response}")
input = json_response.get("input")
question = json_response.get("question")

openai.api_key = OPENAI_API_KEY

output = ""
max_items = 10

for index, string in enumerate(input):
    if index > 0 and index % max_items == 0:
        answer = chat_completion(output, question)
        print(answer)
        output_value = answer.split(':')[1].split('}')[0].replace('"', '').strip()
        if output_value != "BAZINGA":
            break
        output = ""
    output += string + "\n"
if (output_value == "BAZINGA") and output:
    answer = chat_completion(output, question)
    print(answer)
    output_value = answer.split(':')[1].split('}')[0].replace('"', '').strip()
if output_value != "BAZINGA":
    print (output_value)
    data = {
       "answer":output_value
    }
    response = requests.post(URL_AI_DEVS+ANSWER+token, json=data)
    json_response = response.json()
    print (json_response)