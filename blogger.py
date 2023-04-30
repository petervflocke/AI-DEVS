import requests
import sys
import os
import json
import logging
import time
import openai

# Use AI-Devs GPT4 Proxy?
PROXY = False

# Prompt definition
# compatible with gpt-3.5-turbo, do not stick to jason formatting of the answer.
# request to split the gpt response to chapters divided by ### characters
# conduct split of the gpt response into the expected list in python together with some simple syntax checking

# openAI SYSTEM
system_text = """
You are a blog writer. Please write a blog post for the provided outline. Outline consists of list of chapters to be reflected in the post. 
Each chapter starts with the string "###" and the the chapter title.

List of topics follows this data structure:
Topics=['topic 1', 'topic 2', 'topic 3', ...]
"""
# Chapter's splitter, assuming that GPT follows my prompt
SPLITTER = "###"

# openAI user text, the rest wll be concatenated based on the task's request
user_text = "Topics="


def chat_completion(system_text, user_text):
    """
    This function takes two arguments, 'system_text' and 'user_text', and generates a response using the OpenAI ChatCompletion API.

    Args:
    system_text (str): A string containing the system message to set the context for the conversation.
    user_text (str): A string containing the user message to which the function will generate a response.

    Returns:
    str: A message generated by the GPT-3.5-turbo model based on the input messages.

    Example usage:
    >>> system_text = "You are an AI language model."
    >>> user_text = "How does GPT-3.5-turbo work?"
    >>> response = chat_completion(system_text, user_text)
    >>> print(response)
    "GPT-3.5-turbo is a cutting-edge AI model that generates human-like text based on context and input. It works by predicting the next word in a sequence, using deep learning techniques and a vast training dataset."
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
    )
    message = response["choices"][0]["message"]["content"]
    return message


def gpt4_completion(system_text, user_text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PROXY_API_KEY}",
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
    }
    response = requests.post(PROXY_API_URL, headers=headers, data=json.dumps(data))
    json_response = response.json()
    logging.debug("Response from GPT4 AI-Devs: %s", json_response)
    message = json_response["choices"][0]["message"]["content"]
    return message


def split_string(string, div, expected_len=0):
    """
    Splits a long string into a list of substrings using a divider string or character.

    Args:
        string (str): The long string to be split.
        div (str): The divider string or character to split the string with.
        expected_len (int): how many elements is expected

    Returns:
        list: A list of substring resulting from splitting the input string based on the
        divider argument.
    """
    if div == "":
        raise ValueError("Divider can't be empty.")
    if not isinstance(string, str) or not isinstance(div, str):
        raise TypeError("Both arguments should be a string.")

    substrings = string.split(div)
    logging.debug("Splitted text: %s", substrings)
    #Removed first entry, either it is empty when gpt has started from ### or some bla bla before the first chapter
    substrings.pop(0)        
    if expected_len != 0 and len(substrings) != expected_len:
        raise ValueError(
            f"Expected length of the list: {expected_len} does not match current one: {len(substrings)}."
        )

    return substrings


if len(sys.argv) > 1:
    DEBUG_MODE = sys.argv[1]
else:
    # DEBUG_MODE = "debug", "info", anything else for off
    DEBUG_MODE = "off"
if DEBUG_MODE == "debug":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
elif DEBUG_MODE == "info":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
else:
    logging.disable(sys.maxsize)

TASKNAME = os.path.splitext(os.path.basename(__file__))[0]
KEY = os.environ.get("AIDEVS")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
URL_AI_DEVS = os.environ.get("URL_AI_DEVS")

# AI-Devs proxy settings
PROXY_API_URL = os.environ.get("PROXY_API_URL")
PROXY_API_KEY = os.environ.get("PROXY_API_KEY")

TOKEN = "/token/"
TASK = "/task/"
ANSWER = "/answer/"

if not KEY:
    raise ValueError("API KEY cannot be empty, setup environment variable AIDEVS")
if not OPENAI_API_KEY:
    raise ValueError(
        "openAI API KEY cannot be empty, setup environment variable OPENAI_API_KEY"
    )
if not URL_AI_DEVS:
    raise ValueError(
        "URL for AI_devs cannot be empty, setup environment variable URL_AI_DEVS"
    )
if not PROXY_API_URL:
    raise ValueError(
        "URL for AI_devs GPT4 Proxy cannot be empty, setup environment variable PROXY_API_URL"
    )
if not PROXY_API_KEY:
    raise ValueError(
        "URL for AI_devs GPT4 Proxy cannot be empty, setup environment variable PROXY_API_KEY"
    )

logging.debug("Key:%s; TaskName:%s", KEY, TASKNAME)

openai.api_key = OPENAI_API_KEY

data = {
    "apikey": f"{KEY}",
}

response = requests.post(URL_AI_DEVS + TOKEN + TASKNAME, json=data)
json_response = response.json()
logging.info("Received json: %s", json_response)

token = json_response.get("token")
response = requests.get(URL_AI_DEVS + TASK + token)
json_response = response.json()
logging.info("Received json: %s", json_response)

blog = json_response.get("blog")
user_text += json.dumps(blog)
logging.info("Processing: %s chapters...", len(blog))
logging.info("Using %s", "AI-Devs GPT4" if PROXY else "openAI GPT-3.5")
start_time = time.time()
if PROXY:
    answer = gpt4_completion(system_text, user_text)
else:
    answer = chat_completion(system_text, user_text)
end_time = time.time()
duration = end_time - start_time
logging.info("Done after %s seconds", "{:.0f}".format(duration))
answer = split_string(answer, SPLITTER, len(blog))
logging.info("Answer to be sent: %s", answer)
data = {"answer": answer}

sys.exit(1)
response = requests.post(URL_AI_DEVS + ANSWER + token, json=data)
json_response = response.json()
print(json_response)

