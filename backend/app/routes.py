from datetime import datetime

from flask import Blueprint, jsonify, request

from . import db
from .models import Tarefa

main = Blueprint("main", __name__)


@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    try:
        data_formdata = datetime.strptime(data["data_limite"], "%d/%m/%Y").date()
    except ValueError:
        return jsonify({"ERRO,DATA INVÀLIDA.USE DD/MM/AAAA"}), 400

    nova = Tarefa(
        nome=data["nome"],
        custo=data["custo"],
        data_limite=data_formdata,
        ordem=data["ordem"],
    )
    try:
        db.session.add(nova)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"ERRO:NOME OU ORDEM JÀ EXISTENTE"}), 400
    return jsonify({"MSG,TAREFA ENVIADA COM SUCESSO"}), 201


@main.route("/tasks", methods=["GET"])
def list_task():
    tarefas = Tarefa.query.order_by(Tarefa.ordem).all()

    return jsonify(
        [
            {
                "id": t.id,
                "nome": t.nome,
                "custo": float(t.custo),
                "data_limite": t.data_limite.strftime("%d/%m/%Y"),
                "ordem": t.ordem,
            }
            for t in tarefas
        ]
    )
