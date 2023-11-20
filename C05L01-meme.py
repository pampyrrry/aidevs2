import requests
import json
import openai
from openai import OpenAI
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "meme"
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
image_url = task.get('image')
print(image_url)
text = task.get('text')
print(text)
print("Podaj klucz API do rednerform: ")
render_API = input()
io_url = "https://get.renderform.io/api/v2/render"
io_headers = {"X-API-KEY": render_API, "Content-Type": "application/json"}
io_deta = {
    "template": "lean-lions-scream-madly-1986", # Change to your template name !
    "data": {
        "my-text-component-id.color": "#000000",
        "text.text": text,
        "img.src": image_url,
    }
}
image = requests.post(io_url, headers=io_headers, json=io_deta)
print(image.status_code)
print(image.text)
image_response = image.json()
answer = image_response.get("href", None)

answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("*"*30)
