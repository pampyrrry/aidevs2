from flask import Flask
from flask import jsonify
from flask import request
import openai
from openai import OpenAI

app = Flask(__name__)



check = None
@app.route('/', methods=['GET'])
def hi():
    return "AIDevs - ownapipro"


@app.route('/test', methods=['POST'])
def test_post():
    try:
        with open("dane.txt", "r") as file:
            
            data_form_file = file.read()
        print(data_form_file)
        question = request.get_json()
        q = question.get("question")
        print(q)
        gptapi = "__YOUR_API_KEY__"
        openai.api_key = gptapi
        client = OpenAI(api_key=openai.api_key)

        try:
            response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                                      messages=[{"role": "system", "content": "Odp na pytanie zwięźle. Jeśli pytanie będzie wykraczać poza twoją  bazę danych sprawdź odp w 'dodatkowej bazie danych"
                                                                                              "Dodatkowa baza danych````` : "+ data_form_file},
                                                                {"role": "user", "content": f"{q}"}])
            answer = response.choices[0].message.content
            with open("dane.txt", "a") as plik:
                # Zapisywanie informacji do pliku
                plik.write(q + "\n")

            reply = {"reply": f"{answer}"}

            print(reply)
            return reply
        except Exception as e:
            app.logger.error('An error occurred while calling OpenAI API: %s', str(e))
            return 'Error occurred while calling OpenAI API', 500
    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        return 'Internal Server Error', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
