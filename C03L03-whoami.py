import requests
import json
import openai
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "whoami"
url = "https://zadania.aidevs.pl/token/"+nameOfTask
print("Podaj OpenAI API KEY: ")
gptapi = input()
hint = []
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

#Krok 3 Wykonywanie zadania z wykorzystaniem funcji połaczenia z AIDevs i OpenAI API

while True:
    task, token = getting_a_task(url, api)
    print(task)
    hint.append(task["hint"])
    print(hint)
    print("Łączę z ChatGPT")
    openai.api_key = gptapi
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Guess person, Check Hint!. ### Rules if you Know response only Name and Surename, if you don't know response only 0 nothing else!."},
            {"role": "user", "content": f"Gues a person-  Hint: {hint}"}
        ]
    )
    print(response)
    answer = response['choices'][0]['message']['content']
    if answer == "0":
        time.sleep(1)
    else:
        task, token = getting_a_task(url, api)
        answer_url = "https://zadania.aidevs.pl/answer/" + token
        send_response = requests.post(answer_url, json={"answer": answer})
        print(send_response.text)
        break
print("******************************************************")


