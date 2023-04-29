import requests
import sys
import os
import json
import logging

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

URL_AI_DEVS = os.environ.get('URL_AI_DEVS')
TOKEN = "/token/"
TASK = "/task/"
ANSWER = "/answer/"

if not KEY:
    raise ValueError("API KEY cannot be empty, setup environment variable AIDEVS")
if not URL_AI_DEVS:
    raise ValueError("URL for AI_devs cannot be empty, setup environment variable URL_AI_DEVS")

logging.debug(f"Key: {KEY}\nTaskName:{TASKNAME}")


data = {
    "apikey": f"{KEY}",
}

response = requests.post(URL_AI_DEVS+TOKEN+TASKNAME, json=data)
json_response = response.json()
token = json_response.get("token")
logging.info(f"Received token: {token}")

response = requests.get(URL_AI_DEVS+TASK+token)
json_response = response.json()
answer = json_response.get("cookie")
logging.info(f"Received answer: {answer}")

data = {
  "answer":f"{answer}"
}
print (data)

response = requests.post(URL_AI_DEVS+ANSWER+token, json=data)
json_response = response.json()
print (json_response)