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
    return render_template("settings.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
