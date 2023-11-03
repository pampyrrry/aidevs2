import os
import requests
import json
import openai

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Podaj nazwę zadania")
nameOfTask = input()

# KROK 2 wysłanie metodą POST w celu autoryzacji
url = "https://zadania.aidevs.pl/token/"+nameOfTask
print(api)
print(url)
api_to_send = {"apikey": api}
post_response = requests.post(url, json=api_to_send)
post_response = post_response.json()
print(post_response)

# KROK 3 pobranie wartości tokena z JSON i przypisanie go do adresu (metoda GET)
token = post_response.get("token")
get_url = "https://zadania.aidevs.pl/task/"+token
get_response = requests.get(get_url)
get_response_to_json = get_response.json()
#print("G" + get_response_to_json)
#
print("Wprowadź API-Key z ChatGPT")
gptapi = input()
openai.api_key = gptapi

assistant = "You're guardrails system. Answer Only Yes or No. You get pair with 'question : answer'. Check if the answer has on the same subject as the question."

questions = ["What colour is a blue car?", "What is the capital of Poland?", "Did Tolkien write The Hobbit?"]
answer_q = []
pair = []
url_task = "https://adres-api/task/"
for question in questions:
    data = {"question": question}
    response = requests.post(get_url, data=data)
    response_data = response.json()
    print("Odpowiedź: " + response.text)
    #print("Odpowiedź na pytanie '{}': {}".format(question, response_data['answer']))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user",
             "content": "{}: {}".format(question, response_data['answer']) + "Return only Yes or No. Finaly answer only: YES or NO"}
        ]
    )
    print(response)
    to_send = response['choices'][0]['message']['content']
    print(to_send)
    answer_url = "https://zadania.aidevs.pl/answer/" + token
    send_response = requests.post(answer_url, json={"answer": to_send})
    print(send_response.text)
    print("******************************************************")
    #pair.append("{}: {}".format(question, response_data['answer']))
print("-------____---------")



