import os
import requests
import json
import openai

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "whisper"
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
gptapi = input()

audio_url = "https://zadania.aidevs.pl/data/mateusz.mp3"
response = requests.get(audio_url)
with open('audio.mp3', 'wb') as f:
    f.write(response.content)

openai.api_key = gptapi
with open('audio.mp3', 'rb') as f:
    transcript = openai.Audio.transcribe("whisper-1", f)
transcript = transcript.get("text")
print(transcript)

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": transcript})
print(send_response)
print(send_response.text)

print("##########################################")

