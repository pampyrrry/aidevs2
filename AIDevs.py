import requests

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

# Krok 4 pobranie wartości 'answer' z JSON i wysłanie metoda POST
cookie = get_response_to_json.get("cookie")
answer = {"answer": cookie}
answer_url = "https://zadania.aidevs.pl/answer/"+token
answer_response = requests.post(answer_url, json=answer)
print (answer_response.text)
