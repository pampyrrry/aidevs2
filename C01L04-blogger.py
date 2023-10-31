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
print(get_response_to_json)

#
msg = get_response_to_json.get("msg")
blog = get_response_to_json.get("blog")
print(msg)
print(blog)
#
print("Wprowadź API-Key z ChatGPT")
gptapi = input()
openai.api_key = gptapi
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"answer truthfully, as briefly as possible. ###context: {blog}"},
        {"role": "user", "content": msg + '. Use Polish. You have to send ARRAY with only 4 quote as answer. Finally format should looks like: ["tekst 1","tekst 2","tekst 3","tekst 4"] without part from context' }
    ]
)
print(response)
print("#######------------#######")
response04 = response['choices'][0]['message']['content']
print(response04)
response04 = response04.replace("\n", "")
response04 = json.loads(response04)
answer = {"answer": response04}

print(answer)
answer_url = "https://zadania.aidevs.pl/answer/"+token
send_response = requests.post(answer_url, json=answer)
print(send_response.text)