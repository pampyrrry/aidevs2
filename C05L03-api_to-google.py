from flask import Flask
from flask import jsonify
from flask import request
from serpapi import GoogleSearch

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hi():
    return "AIDevs - google"


@app.route('/test', methods=['POST'])
def test_post():
    try:
        question = request.get_json()
        question_api = question.get("question")
        print(question_api)

        params = {
            "engine": "google",
            "q": f"{question_api}",
            "api_key": "__YOUR_API_KEY"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"][0]["link"]
        reply = {"reply": f"{organic_results}"}
        print(reply)

        return reply

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        return 'Internal Server Error', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
