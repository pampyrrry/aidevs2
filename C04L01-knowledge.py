import requests
import json
import openai
import time


# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "knowledge"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

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

def currency(question):
    currency = "http://api.nbp.pl/api/exchangerates/tables/A"
    resonse_currency = requests.get(currency)
    json_currency = resonse_currency.json()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Reply value of currency only. #### Your details for a reply:: Current currency:{json_currency}. ###Reply onli number nothin else"
                        f"###Example: 4.1474"},
            {"role": "user", "content": f": {question}"}
        ]
    )
    return response['choices'][0]['message']['content']

def population(question):
    code_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You reply only about country topic. Reply only CODE OF COUNTRY #### Example:"
                        f"user: What is population of France?,  assistant: fr - nothing else. Return ONLY CODE"},
            {"role": "user", "content": f": {question}"}
        ]
    )
    code = code_response['choices'][0]['message']['content']
    countries = f"https://restcountries.com/v3.1/alpha/{code}"
    print("KOD:" + code)
    resonse_countries = requests.get(countries)
    json_countries = resonse_countries.json()
    population = json_countries[0]["population"]
    print("Population: " + str(population))
    pop_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"Reply only NUMBER#### Your details for a reply:: {population}"
                        f"###Example: 83340525 - NUMBER Numbers without separators"},
            {"role": "user", "content": f": {question}"}
        ]
    )
    return pop_response['choices'][0]['message']['content']


task, token = getting_a_task(url, api)
print(task)
question = task.get('question')
print(question)
print("Podaj OpenAI API KEY: ")
gptapi = "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"
openai.api_key = gptapi
task, token = getting_a_task(url, api)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",
         "content": f"You have to choose the type of question and response only ONE WORD from the list. ###LIST 3 types of question: CURRENCY , POPULATION , GENERAL"
                    f"###Keep question style of answer! Nothing else!"},
        {"role": "user", "content": f": {question}"}
    ]
)
print(response)
answer = response['choices'][0]['message']['content']
print(answer)
result = None
if answer == "CURRENCY":
    result = currency(question)
elif answer == "POPULATION":
    result = population(question)
else:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are assistant. Answer the question full senstence"},
            {"role": "user", "content": f": {question}"}
        ]
    )
    result = response['choices'][0]['message']['content']
print(result)

answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": result})
print(send_response.text)
print("******************************************************")


