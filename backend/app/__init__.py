import os
from datetime import date

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

    database_url = os.environ.get("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Tarefa  # garante que o model seja carregado

    with app.app_context():
        db.create_all()

        if Tarefa.query.count() == 0:
            tarefas_exemplo = [
                Tarefa(
                    nome="Planejar projeto",
                    custo=500,
                    data_limite=date(2026, 2, 10),
                    ordem=1,
                ),
                Tarefa(
                    nome="Implementar backend",
                    custo=1200,
                    data_limite=date(2026, 2, 15),
                    ordem=2,
                ),
                Tarefa(
                    nome="Criar interface",
                    custo=800,
                    data_limite=date(2026, 2, 20),
                    ordem=3,
                ),
            ]

            db.session.add_all(tarefas_exemplo)
            db.session.commit()
            print("✅ Tarefas de exemplo criadas")

    from .routes import main

    app.register_blueprint(main)

    return app
