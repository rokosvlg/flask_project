# -*- coding: UTF-8 -*-
import os
from flask import *
import uuid
from flask_login import *

import settings

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SECRET_KEY'] = settings.SECRET_KEY

manager = LoginManager(app)

if __name__ == "__main__":
    from controller import app
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5057, debug=True)
