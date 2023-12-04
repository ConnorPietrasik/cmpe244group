from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import embed_stuff as fan
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        goal_temp = request.form.get("goal_temp")
        with open(fan.doc_root + "goal_temp.txt","w") as f:
            f.write(goal_temp)
        fan.goal_temp = float(goal_temp)
    return render_template("index.html", cur_temp=fan.cur_temp, goal_temp=fan.goal_temp)

#Should be post, but time
@app.route("/stop", methods=["GET"])
def stop_system():
    fan.stop()
    return "Fan system stopped!", 200

#Should be post, but time
@app.route("/start", methods=["GET"])
def start_system():
    if fan.enable:
        return "System already on!", 409
    fan.start()
    return "Fan system started!", 200

#For testing
@app.route("/setcur/<val>", methods=["GET"])
def set_cur_temp(val):
    fan.cur_temp = float(val)
    return f"Cur temp set to {val}", 200

#Expects json body, "goal_temp": {float}
@app.route("/goal", methods=["POST"])
def set_goal():
    goal_temp = request.get_json()["goal_temp"]
    with open(fan.doc_root + "/goal_temp.txt","w") as f:
        f.write(goal_temp)
        fan.goal_temp = goal_temp
    return "Success!", 200

@app.route("/goal", methods=["GET"])
def get_goal():
    return jsonify({"goal_temp": fan.goal_temp}), 200

@app.route("/chat", methods=["GET"])
def get_chat():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def post_chat():
    client = OpenAI()
    req = request.form.get("user_input")
    if req: 
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[ {"role": "system", "content": "You are Johnny, the CTI One technical support for CMPE244_FAN_SYSTEM."},
                       {"role": "user", "content": req}] 
        ) 
        reply = chat.choices[0].message.content 
        token_cost = chat.usage.total_tokens
        print(f"User: {req}\nChatGPT: {reply}\nCost: {token_cost}") 

    return render_template("chat.html", reply=reply)


#Init stuff here because WSGI
fan.init()
load_dotenv(dotenv_path=fan.doc_root + "/.env")

if __name__ == "__main__":
    app.run("0.0.0.0", 80)