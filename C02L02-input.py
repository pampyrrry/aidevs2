import os
import requests
import json
import openai

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "inprompt"

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
print(get_response_to_json)
find_name = get_response_to_json["question"]
input_table = get_response_to_json["input"]
print(find_name)
print(input_table)
#
print("Wprowadź API-Key z ChatGPT")
gptapi = input()
openai.api_key = gptapi
assistant = "You're my assistant. Answer only the name (one word)"
url_task = "https://adres-api/task/"
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user",
             "content": "Find a name of person in this question: "+find_name}
        ]
    )
print(response)
name = response['choices'][0]['message']['content']
print(name)

def find_sentence_with_name(input_table, name):
    for sentence in input_table:
        if name in sentence:
            return sentence
    return "Nie znaleziono słowa"

sentence = find_sentence_with_name(input_table, name)

print(sentence)

response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": assistant + "###context: "+sentence},
            {"role": "user",
             "content": "Answer on the question: "+find_name}
        ]
    )
print(response)
answer = response['choices'][0]['message']['content']
print(answer)

answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("******************************************************")




