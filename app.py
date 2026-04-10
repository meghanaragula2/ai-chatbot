from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__)

# 🔑 STEP: Add your API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        reply = response["choices"][0]["message"]["content"]

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)