import os
import json
import requests

url = os.environ.get("PROXY_API_URL")

#To nie dziala
system_text = """
You are a blog writer. Please write a blog post for the provided outline. Outline consists of list of chapters to be reflected in the post. 
Each chapter starts with the string "###" and the the chapter title.

List of topics follows this data structure:
Topics=['topic 1', 'topic 2', 'topic 3', ...]
"""

user_text = """
Topics=['Wstęp: kilka słów na temat historii pizzy', 'Niezbędne składniki na pizzę', 'Robienie pizzy', 'Pieczenie pizzy w piekarniku']
"""


#To dziala:

# system_text = """
# You name is Jakub. Always answer only with your name.
# """
# user_text = """
# What's your name?
# """

# To dziala

# system_text = """
# """
# user_text = """
# Say this is a test!
# """





headers = {
    "Content-Type": "application/json",
}
data = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ],
    "temperature": 0.7,
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print (response)
json_response = response.json()
print (json_response)
message = json_response["choices"][0]["message"]["content"]
print (message)
