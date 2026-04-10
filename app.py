from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Simple knowledge base
responses = {
    "hello": ["Hi! 👋", "Hello there!", "Hey! How can I help you?"],
    "how are you": ["I'm good 😊", "Doing great!", "All good here!"],
    "what is your name": ["I am your AI chatbot 🤖"],
    "bye": ["Goodbye! 👋", "See you soon!", "Take care!"],
}

def get_response(user_input):
    user_input = user_input.lower()

    for key in responses:
        if key in user_input:
            return random.choice(responses[key])

    # default response
    return "Sorry, I didn't understand that. Try asking something else 😊"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    reply = get_response(user_input)
    return jsonify({"response": reply})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)