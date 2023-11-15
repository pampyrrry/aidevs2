import requests
import json
import openai
from openai import OpenAI
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "gnome"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

def getting_a_task(url, api):
    api_to_send = {"apikey": api}
    post_response = requests.post(url, json=api_to_send)
    post_response = post_response.json()
    token = post_response.get("token")
    url_to_task = "https://zadania.aidevs.pl/task/" + token
    get_task = requests.get(url_to_task)
    task_to_json = get_task.json()
    return task_to_json, token

task, token = getting_a_task(url, api)
print(task)
url_image = task.get('url')
print(url_image)

print("Podaj OpenAI API KEY: ")
gptapi = input()
openai.api_key = gptapi
client = OpenAI(api_key=openai.api_key)

task, token = getting_a_task(url, api)

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Tell me what is the color of the hat in POLISH?"
                                 "If any errors occur, return 'ERROR' as answer' Reply only one word Color or ERROR"},
        {
          "type": "image_url",
          "image_url": {
            "url": url_image,
          },
        },
      ],
    }
  ],
  max_tokens=300,
)
print(response)
answer = response.choices[0].message.content
print(answer)

answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("*"*30)


