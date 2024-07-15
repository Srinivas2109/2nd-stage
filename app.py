from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
import openai
from decision_logic import is_flagged_question

# Load environment variables from .env
load_dotenv()

# URL of the first project's Flask service
FLASK_SERVICE_URL = os.getenv("FLASK_SERVICE_URL", "http://127.0.0.1:5000/chat")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

def openai_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",  # or use "gpt-4" if you have access
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("user_input")

    if is_flagged_question(user_input):
        response = requests.post(FLASK_SERVICE_URL, json={"user_input": user_input})
        if response.status_code == 200:
            return jsonify({"response": response.json().get("response")})
        else:
            return jsonify({"error": response.json().get("error")})
    else:
        response = openai_chatbot_response(user_input)
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
