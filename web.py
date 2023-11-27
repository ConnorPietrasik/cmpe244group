from flask import Flask, render_template, request
app = Flask(__name__)
 
@app.route("/", methods=["GET"])
def index():
    with open("cur_temp.txt","r") as f:
        cur_temp = f.read()
    return render_template('index.html', cur_temp=cur_temp)

@app.route("/", methods=["POST"])
def posted():
    goal_temp = request.form.get("goal_temp")
    with open("goal_temp.txt","w") as f:
        f.write(goal_temp)
    with open("cur_temp.txt","r") as f:
        cur_temp = f.read()
    return render_template('index.html', cur_temp=cur_temp)
 
if __name__ == "__main__":
    app.run(host="0.0.0.0")