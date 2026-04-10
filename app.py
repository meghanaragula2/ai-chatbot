from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Free public API (no key needed)
API_URL = "https://api-inference.huggingface.co/models/gpt2"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    try:
        response = requests.post(
            API_URL,
            json={"inputs": user_input}
        )

        if response.status_code != 200:
            return jsonify({"response": "API Error: " + response.text})

        data = response.json()

        if isinstance(data, list):
            reply = data[0].get("generated_text", "No response")
        else:
            reply = str(data)

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"response": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)