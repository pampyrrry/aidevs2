import requests
import json

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "functions"
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

# Funkcja która zosytała by wywołana przez "functionCalling"
def addUsers (name, surname, year):
    user = {
        "name": name,
        "surname": surname,
        "year": year
    }
    return user
# ciało funkcji -> więcej na: https://platform.openai.com/docs/guides/gpt/function-calling
addUser = {
    "name": "addUsers",
    "description": "Add a new user to my base",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "provide the name of user"
            },
            "surname": {
                "type": "string",
                "description": "provide the surname of user"
            },
            "year": {
                "type": "integer",
                "description": "provide the year of born"
            }
        }
    }
}
print(addUser)

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": addUser})
print(send_response)
print(send_response.text)

print("##########################################")