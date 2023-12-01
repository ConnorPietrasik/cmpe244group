from flask import Flask, render_template, request
from openai import OpenAI
import lgpio
from time import sleep
from threading import Thread
from queue import Queue

app = Flask(__name__)

command = Queue()

def spin_motor(clockwise = True, delay = 0.004, step_max = 4096, con = [17, 27, 22, 23]):
    #Half-step, so step_max = 4096 for full rotation
    steps = [
        0b1001,
        0b1000,
        0b1100,
        0b0100,
        0b0110,
        0b0010,
        0b0011,
        0b0001
    ]

    h = lgpio.gpiochip_open(0)
    lgpio.group_claim_output(h, con)

    try:
        step = 0
        while command.empty():
            lgpio.group_write(h, con[0], steps[step])
            step = (step - 1) % 8 if clockwise else (step + 1) % 8
            sleep(delay)
    except Exception:
        lgpio.group_write(h, con[0], 0)
        lgpio.group_free(h, con[0])
        lgpio.gpiochip_close(h)
        exit(1)


def testy():
    while command.empty():
        print("Testing!")
        sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():

    command.put("tomato")
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

    t = Thread(target=spin_motor, kwargs={"delay": 0.1})
    t.start()

    app.run(host="0.0.0.0")