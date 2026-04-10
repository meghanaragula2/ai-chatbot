from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔑 Get API key from environment (Render)
API_KEY = os.getenv("HF_API_KEY")

# ✅ Working Hugging Face model (free + stable)
API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": user_input}
        )

        # ❗ If API fails
        if response.status_code != 200:
            return jsonify({"response": f"API Error: {response.text}"})

        try:
            data = response.json()
        except:
            return jsonify({"response": "Model is loading... please wait ⏳"})

        # ✅ Handle response
        if isinstance(data, list):
            reply = data[0].get("generated_text", "No response")
        elif isinstance(data, dict) and "error" in data:
            reply = "Model is loading or busy... try again ⏳"
        else:
            reply = str(data)

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"response": reply})


# 🚀 IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)