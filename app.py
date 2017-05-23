from flask import Flask, render_template, request
import datetime

from utils.security import security

app = Flask(__name__)
app.secret_key = "patrickchan"
app.register_blueprint(security.security)

@app.route("/")
def root():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    #seconds = 31490 #second period
    seconds = 37190 #Passing
    #seconds = 52000 #9th period
    #seconds = 55000 #10th period
    #seconds = 56100 #switching to afterschool
    #seconds = 28800 #beginning of the day
    return render_template("schedule.html", starttime = str(seconds), schedulename = "Regular Schedule")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
