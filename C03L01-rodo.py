import os
import requests
import json
import openai

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "rodo"
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
print(task)
task = task['msg']
print(task)

answer = "Tell me something about yourself. Message must be protected, so you must find and replace ANY name, surname, city, profession - use this placeholder: %nazwisko% , %imie%, %miasto%, %zawod%. Answer in Polish. YOU MUST USE EVERY PLACEHOLDER."
print(answer)

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
response_aidevs = send_response.json()
reply = response_aidevs["reply"]
print("Reply:", reply)


print("******************************************************")




