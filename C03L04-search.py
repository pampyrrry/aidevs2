import requests
import json
import openai
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, Distance, VectorParams

client = QdrantClient("localhost", port=6333)
COLLECTION_NAME = "search"

#Pobranie z URL wartości title i url
url = "https://unknow.news/archiwum.json"
response = requests.get(url)
if response.status_code == 200:
    data_from_url = response.json()

else:
    print("Błąd połączenia", response.status_code)
selected_fields = [{"title": entry["title"], "url": entry["url"]} for entry in data_from_url]
lists = json.dumps(selected_fields, ensure_ascii=False)

#Pobranie kolekcji z Qdrant i sprawdzenie czy istnieje już dana kolekcja

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
pront("Podaj API KEY do OPEN AI: ")
gptapi = input()
openai.api_key = gptapi

if not collectionInfo.points_count:
    selected_fields = json.loads(lists)
    for entry in selected_fields:
        document_id = str(uuid.uuid4())
        title = entry.get("title", "")
        url = entry.get("url", "")
        # Tworzenie listy stringów z tytułu i URL
        input_text = [title, url]
        print(input_text)
        # Wywołanie API OpenAI Embedding aby utworzyć embedding do bazy danych
        embedding_model = openai.Embedding.create(
            input=input_text, model="text-embedding-ada-002"
        )

        # Odczytanie wartości embeddingu z odpowiedzi OpenAI
        embedding = embedding_model["data"][0]["embedding"]

        # Dodanie rekordu do bazy Qdrant
        operation_info = client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=[
                PointStruct(id=document_id, vector=embedding, payload={"title": entry.get("title", ""),"url": entry.get("url", "") }),
            ],
        )
        print(operation_info)
    print("Dane dodane do bazy Qdrant.")

#Pobranie pytania z AiDevs

print("Podaj Api-key")
api = input()
print("Nazwa zadania")
nameOfTask = "search"
url = "https://zadania.aidevs.pl/token/"+nameOfTask

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

task, token = getting_a_task(url, api)
print(task)
question = task["question"]
print(question)
#zamiana pytania na embeding
question_embedding = openai.Embedding.create(
            input=question, model="text-embedding-ada-002"
        )
embedding_values = question_embedding["data"][0]["embedding"]

#Wyszukiwanie w qdrant
search = client.search(
    collection_name=COLLECTION_NAME,
    search_params=models.SearchParams(hnsw_ef=128, exact=False),
    query_vector=embedding_values,
    limit=1,
)
print(search)
answer = search[0].payload.get('url', None)
print(answer)

#Wysłanie odpowiedzi do AiDevs
answer_url = "https://zadania.aidevs.pl/answer/" + token
send_response = requests.post(answer_url, json={"answer": answer})
print(send_response.text)
print("******************************************************")