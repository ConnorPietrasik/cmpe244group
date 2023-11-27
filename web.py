from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        goal_temp = request.form.get("goal_temp")
        with open("goal_temp.txt","w") as f:
            f.write(goal_temp)
    with open("cur_temp.txt","r") as f:
        cur_temp = f.read()
    with open("goal_temp.txt","r") as f:
        goal_temp = f.read()
    return render_template("index.html", cur_temp=cur_temp, goal_temp=goal_temp)

@app.route("/chat", methods=["GET"])
def get_chat():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def post_chat():
    client = OpenAI()
    reply = request.form.get("user_input")
    if reply: 
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[ {"role": "system", "content": "You are Johnny, the CTI One technical support for CMPE244_FAN_SYSTEM."},
                       {"role": "user", "content": reply}] 
        ) 
        reply = chat.choices[0].message.content 
        token_cost = chat.usage.total_tokens
        print(f"ChatGPT: {reply}\nCost: {token_cost}") 

    return render_template("chat.html", reply=reply)

 
if __name__ == "__main__":
    app.run(host="0.0.0.0")