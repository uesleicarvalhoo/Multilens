from flask import Flask
from multilens.ext import config, cli, db, site, admin

def create_app():
    app = Flask(__name__)
    config.init_app(app)
    db.init_app(app)
    cli.init_app(app)
    site.init_app(app)
    admin.init_app(app)

    return app
