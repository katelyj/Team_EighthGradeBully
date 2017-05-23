from flask import Flask, render_template, request

from utils.security import security
from utils.views import public_views

app = Flask(__name__)
app.secret_key = "patrickchan"
app.register_blueprint(security.security)
app.register_blueprint(public_views.public_views)


@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
