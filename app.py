import datetime
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Load AI model
model_name = "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history_ids = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history_ids

    user_input = request.json["message"]
 
    with open("chat.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - User: {user_input}\n")

    with open("chat.txt", "a") as f:
         f.write(user_input + "\n")


    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.75
    )

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    with open("chat.txt", "a") as f:
         f.write(f"{datetime.datetime.now()} - User: {user_input}\n")
    
    with open("chat.txt", "a") as f:
         f.write(user_input + "\n")

    return jsonify({"response": response})

if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)