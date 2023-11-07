import requests
import json
import openai
import time

# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "scraper"
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
print(task)
# pobranie danych z zadania i przypisanie ich do zmiennych.
article_adress = task['input']
print(article_adress)
question = task['question']
msg = task['msg']
print(question)
print(msg)
# Pobranie zawartości tesktu z obsługą błędów
content = None
while True:
    try:
        #dodanie header aby request zachowywał się jak przeglądarka
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Connection': 'keep-alive',
        }
        article = requests.get(article_adress, headers=headers)
        content = article.text
        print(content)
        if content == "server error X_X":
            print("Błąd serwera. Ponowne wysłanie żądania.")
            time.sleep(2)
        else:
            break
    except requests.exceptions.HTTPError as http_error:
        print(http_error)
        time.sleep(2)
    except Exception as e:
        print(f'Inny błąd: {e}')
        time.sleep(2)
print("_/\____________/\_________/")
print(article)
print(content)
#połączenie z ChatGPT aby wysłać artykuł i pytanie
print("Łączę z ChatGPT. Podaj API KEY: ")
gptapi = input()
openai.api_key = gptapi
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Answer based only provided article. Answer truthfully, as briefly as possible. Max 200 characters! ###Rules: Use Polish"},
        {"role": "user", "content": msg +"Article: " + content + "Question: " + question}
    ]
)
print(response)
print("#######------------#######")
answer = response['choices'][0]['message']['content']
print(answer)

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)

print("******************************************************")




