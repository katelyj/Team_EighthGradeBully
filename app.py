from flask import Flask, render_template, request

#from lib.security import security

app = Flask(__name__)
app.secret_key = "patrickchan"
#app.register_blueprint(security.security)

@app.route("/")
def root():
    return render_template("schedule.html")

@app.route("/settings")
def settings():
    return render_tempalte("settings.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
