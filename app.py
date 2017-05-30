from flask import Flask, render_template, request, session, url_for

from lib.security import security
from lib.views import public_views
from lib.views import ajax_views

app = Flask(__name__)
app.secret_key = "patrickchan"
app.register_blueprint(security.security)
app.register_blueprint(public_views.public_views)
app.register_blueprint(settings_views.settings_views)
app.register_blueprint(ajax_views.ajax_views)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
