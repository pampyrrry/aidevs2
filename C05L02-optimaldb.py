import requests
import json
import openai
from openai import OpenAI
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "optimaldb"
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
database = task.get('database')
print(database)
text = requests.get(database)
text_to_cut = text.text
print(text_to_cut)

print("Podaj klucz API: ")
gptapi = input()

openai.api_key = gptapi
client = OpenAI(api_key=openai.api_key)
response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",

  messages=[
    {"role": "system", "content": "Optymalizujesz bazę danych"
                                  "skróć tekst o 50% "
                                  "Musisz zachować wszystkie informację:"
                                  "Tytuły filmów, książek, gry, zawód, miejsce pracy, "
                                  "pierwszy taniec na ślubie, inspiracje."
                                  "Zwróć string!"},
    {"role": "user", "content": "skróć tekst o 50% " + text_to_cut}
  ]
)
print(response.choices[0].message.content)
answer = response.choices[0].message.content
print(answer)
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("*"*30)
