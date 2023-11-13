import requests
import json
import openai
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, Distance, VectorParams
# KROK 1 - wstępne dane
print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "people"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

client = QdrantClient("localhost", port=6333)
COLLECTION_NAME = "people"

collections_response = client.get_collections()
existing_collections_list = collections_response.collections
existing_collection_names = [collection.name for collection in existing_collections_list]

if COLLECTION_NAME in existing_collection_names:
    print(f"Kolekcja o nazwie {COLLECTION_NAME} już istnieje.")
    indexed = client.get_collection(COLLECTION_NAME)
else:
    # Utwórz kolekcję, tylko jeśli nie istnieje
    indexed = client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE, on_disk=True),
    )
    print(f"Utworzono kolekcję o nazwie {COLLECTION_NAME}.")

collectionInfo = client.get_collection(COLLECTION_NAME)
print(collectionInfo)


url_people = "https://zadania.aidevs.pl/data/people.json"
response = requests.get(url_people)
data_from_url = None
if response.status_code == 200:
    data_from_url = response.json()
else:
    print("Błąd połączenia", response.status_code)

#Łączenie z OpenAI API, generowanie embeddingów, dodawanie wektorów i danych
gptapi = input()
openai.api_key = gptapi
if not collectionInfo.points_count:
    for person in data_from_url:
        print(person)
        name_to_embedding = person["imie"] + " " + person['nazwisko']
        print(name_to_embedding)
        embedding_model = openai.Embedding.create(
            input=name_to_embedding, model="text-embedding-ada-002"
        )
        # Odczytanie wartości embeddingu z odpowiedzi OpenAI
        embedding = embedding_model["data"][0]["embedding"]
        #numer ID
        document_id = str(uuid.uuid4())
        # Dodanie rekordu do bazy Qdrant
        operation_info = client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=[
                PointStruct(id=document_id, vector=embedding,
                            payload=person),
            ],
        )
        print(operation_info)
    print("Dane dodane do bazy Qdrant.")

# Pobranie treści zadania i pytania

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
question = task["question"]
print(question)

# Generowanie embeddingu z pytania
question_embedding = openai.Embedding.create(
            input=question, model="text-embedding-ada-002"
        )
embedding_values = question_embedding["data"][0]["embedding"]

#Wyszukiwanie w Qdrant
search = client.search(
    collection_name=COLLECTION_NAME,
    search_params=models.SearchParams(hnsw_ef=128, exact=False),
    query_vector=embedding_values,
    limit=1,
)
print(search)

#Obsługa odpowiedzi
payload = None
for ask in search:
    payload = ask.payload
    print(payload)
response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are {payload}"},
            {"role": "user", "content": question}
        ]
    )
print(response)
answer = response['choices'][0]['message']['content']

# Wysłanie odpowiedzi w formacie JSON
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("******************************************************")




