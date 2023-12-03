import requests
import json
import openai
from openai import OpenAI
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "md2html"
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

task, token = getting_a_task(url, api)


answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": "https://your_adress/api"})
print(send_response.text)
print("*"*30)
