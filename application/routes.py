from . import flask_app
from flask import redirect, render_template, url_for, request, make_response
import json
import pandas as pd


def save_quiz_results(data: dict):
    # df = pd.read_csv("data.csv")
    # Make data frame of above data
    df = pd.DataFrame(data)
    # append data frame to CSV file
    df.to_csv('data.csv', mode='a', index=False, header=False)
    print(f"{df=}")


def get_quiz(number):
    with open("quiz.json", "r") as f:
        quiz_data = json.load(f) 
    if number > len(quiz_data):
        return False 
    return quiz_data[number-1]


@flask_app.get("/")
def index():
    number=1
    quiz=get_quiz(number)
    if quiz:
        return render_template("index.html", title="Simple QUIZ", number=number, quiz=get_quiz(number))

@flask_app.post("/quiz")
def on_after_select():
    answer = request.json.get("answer")
    number = request.json.get("number")
    resp = make_response(redirect(url_for('on_before_select', number=int(number)+1)))
    resp.set_cookie(number, answer)
    print(f"{request.cookies.get('2')=}")
    if request.cookies.get("2"):
        save_quiz_results(request.cookies)
    return resp

@flask_app.get("/quiz/<int:number>")
def on_before_select(number: int):
    
    quiz=get_quiz(number)
    number+=1
    if quiz:
        return render_template("index.html", title="Simple QUIZ", number=number, quiz=get_quiz(number))
    return redirect(url_for('index'))
