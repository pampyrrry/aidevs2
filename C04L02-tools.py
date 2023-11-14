import requests
import json
import openai
import time
# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "tools"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

# KROK 2 Funkcje potrzebne do wykonania zadania
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
question = task.get('question')
print(question)

print("Podaj OpenAI API KEY: ")
gptapi = input()
openai.api_key = gptapi
task, token = getting_a_task(url, api)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system",
         "content": "Decide whether the task should be added to the ToDo list or to the calendar (if time is provided) and return the corresponding JSON"
                    "hint### always use YYYY-MM-DD format for dates, IMPORTANT### to day is: 2023-11-15"
                    'examples###: for ToDo: Przypomnij mi, że mam kupić mleko = "tool":"ToDo","desc":"Kup mleko"'
                    'for calendar:Jutro mam spotkanie z Marianem = "tool":"Calendar","desc":"Spotkanie z Marianem","date":"2023-11-15"'},
        {"role": "user", "content": f": {question}"}
    ]
)
result = response['choices'][0]['message']['content']
to_json = json.loads(result)

print(to_json)

answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": to_json})
print(send_response.text)
print("*"*30)


