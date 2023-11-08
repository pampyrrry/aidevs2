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

def gpt_conversation(hint, gptapi):
    task, token = getting_a_task(url, api)
    print(task)
    hint_to_add = task["hint"]
    hint.append(hint_to_add)
    print(hint_to_add)
    # połączenie z ChatGPT aby wysłać artykuł i pytanie
    print("Łączę z ChatGPT")
    openai.api_key = gptapi
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Guess My name, Check Hint!. ### Rules if you Know response only Name and Surename, if you don't know response only NO nothing else!. Hint: {', '.join(hint)}"},
            {"role": "user", "content": "Gues my name"}
        ]
    )
    print(response)
    print("#######------------#######")
    answer = response['choices'][0]['message']['content']
    print(answer)
    return answer, hint

#Krok 3 Wykonywanie zadania z wykorzystaniem funcji połaczenia z AIDevs i OpenAI API
hint = []
while True:
    gpt, hint = gpt_conversation(hint, gptapi)
    answer = gpt
    if answer == "NO" or answer == "No":
        time.sleep(1)
    else:
        task, token = getting_a_task(url, api)
        answer_url = "https://zadania.aidevs.pl/answer/" + token
        send_response = requests.post(answer_url, json={"answer": answer})
        print(send_response.text)
        break
print("******************************************************")


