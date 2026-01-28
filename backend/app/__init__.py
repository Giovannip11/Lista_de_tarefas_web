import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# start do projeto, subindo o app e bd
def create_app():
    app = Flask(__name__)
    CORS(app)

    basedir = os.path.abspath(os.path.dirname(__file__))

    instance_path = os.path.join(basedir, "instance")
    os.makedirs(instance_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        instance_path, "tarefas.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import Tarefa  # garante que o model seja carregado

    with app.app_context():
        db.create_all()

    from .routes import main

    app.register_blueprint(main)

    return app
