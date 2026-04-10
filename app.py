from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔑 Get API key from Render
API_KEY = os.getenv("HF_API_KEY")

# Hugging Face model (light + free)
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": user_input}
        )

        data = response.json()

        if isinstance(data, list):
            reply = data[0]["generated_text"]
        else:
            reply = "Error: " + str(data)

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"response": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)