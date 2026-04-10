from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("HF_API_KEY")

# ✅ WORKING ENDPOINT (no router issues)
API_URL = "https://huggingface.co/api-inference/models/microsoft/DialoGPT-small"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": user_input,
                "parameters": {"max_new_tokens": 50}
            }
        )

        # 🔍 Debug
        if response.status_code != 200:
            return jsonify({"response": "API Error: " + response.text})

        data = response.json()

        if isinstance(data, list):
            reply = data[0].get("generated_text", "No response")
        elif isinstance(data, dict) and "error" in data:
            reply = data["error"]
        else:
            reply = str(data)

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"response": reply})



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)