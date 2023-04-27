import requests
import sys
import os
import json
import logging

def moderate_text(OPENAI_API_KEY, to_be_moderated):
    MODERATION_API = "https://api.openai.com/v1/moderations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "input": to_be_moderated
    }
    logging.info(f"Data for moderation: {json.dumps(data)}")
    response = requests.post(MODERATION_API, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        json_response = response.json()
        logging.info(f"Received json from moderation endpoint: {json_response}")
        flagged = json_response['results'][0]['flagged']
        return 1 if flagged else 0
    else:
        response.raise_for_status()

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

answer = [];
for value in input:
    flag = moderate_text(OPENAI_API_KEY, value)
    logging.info(f"Text '{value} is Flagged as: {flag}")
    print (f"Text {value} flagged as {flag}")
    answer.append(flag)

print (answer)

data = {
  "answer":answer
}
print (data)

response = requests.post(URL_AI_DEVS+ANSWER+token, json=data)
json_response = response.json()
print (json_response)