from flask import Flask
from flask import jsonify
from flask import request
import openai
from openai import OpenAI
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hi():
    return "Hello"


@app.route('/test', methods=['POST'])
def test_post():
    question = request.get_json()
    print(question)
    q = question.get('question')
    print(q)
    gptapi = "__YOUR_API_KEY__"
    openai.api_key = gptapi
    client = OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",

        messages=[
            {"role": "system", "content": "Odpowiedź na pytanie"},
            {"role": "user", "content": f"{q}"}
        ]
    )
    answer = response.choices[0].message.content
    print(answer)

    return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
