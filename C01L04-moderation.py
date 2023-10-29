import requests
import json

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

# Krok 4 wprowadzenie własnego klucza API
print("Podaj swój klucz API: ")
my_api_key = input()

# Krok 5 pobranie wartości 'input' z JSON i wysłanie metoda POST na endpoint "../moderation"
task_input = get_response_to_json.get("input")
print(task_input)
url = 'https://api.openai.com/v1/moderations'

headers = {
    "Content-Type": "application/json",
    'Authorization': 'Bearer ' +my_api_key,
}
print("Odpowiedź")
answer_data = {"answer": []}
for single_input in task_input:
    data = {
        'input': single_input,
        #'model': 'text-moderation-stable' - jeśli zostanie ustawiony model "...stable" odtrzymujemy po wysłaniu odpowiedzi Respone [400]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        moderation_result = response.json()
        answer_data["answer"].append(1 if moderation_result["results"][0]["flagged"] else 0)
        print(moderation_result)
    else:
        answer_data["answer"].append(0)

#Krok 6 wysłanie odpowiedzi
response_json = json.dumps(answer_data)
print(response_json)
answer_url = "https://zadania.aidevs.pl/answer/"+token
response04 = requests.post(answer_url, response_json)
print(response04.status_code)
