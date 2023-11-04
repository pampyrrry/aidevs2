import os
import requests
import json
import openai

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "embedding"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

# KROK 2 pobranie treści zadania

def getting_a_task(url, api):
    api_to_send = {"apikey": api}
    post_response = requests.post(url, json=api_to_send)
    post_response = post_response.json()
    token = post_response.get("token")
    url_to_task = "https://zadania.aidevs.pl/task/" + token
    get_task = requests.get(url_to_task)
    task_to_json = get_task.json()
    return (task_to_json, token)

task, token = getting_a_task(url, api)
print (task)

# KROK 3 Połączenie z ChatGPT API w celu wykonania zadania

print("Wprowadź API-Key z ChatGPT")
gptapi = input()
openai.api_key = gptapi
response = openai.Embedding.create(
    input="Hawaiian pizza",
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']
print(embeddings)

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": embeddings})
print(send_response.text)
print("******************************************************")




