import os
import json
import requests

url = os.environ.get("PROXY_API_URL")

#To nie dziala
system_text = """
You are a blog writer. Please write one blog post, not more than 3 sentences on the provided topic. 
"""

user_text = """
Topic: 'Wstęp: kilka słów na temat historii pizzy'
"""






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
