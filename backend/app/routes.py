from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import func

from . import db
from .models import Tarefa

main = Blueprint("main", __name__)


@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    if not all(k in data for k in ("nome", "custo", "data_limite")):
        return jsonify({"erro", "Campos obrigatŕios ausentes"}), 400

    try:
        data_formdata = datetime.strptime(data["data_limite"], "%d/%m/%Y").date()
    except ValueError:
        return jsonify({"erro", "DATA INVÁLIDA"}), 400

    ultima_ordem = db.session.query(func.max(Tarefa.ordem)).scalar()
    nova_ordem = (ultima_ordem or 0) + 1

    nova = Tarefa(
        nome=data["nome"],
        custo=data["custo"],
        data_limite=data_formdata,
        ordem=nova_ordem,
    )
    try:
        db.session.add(nova)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"ERRO:NOME OU ORDEM JÀ EXISTENTE"}), 400
    return jsonify({"MSG", "TAREFA ENVIADA COM SUCESSO"}), 201


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
                "destaque": float(t.custo) >= 1000,
            }
            for t in tarefas
        ]
    )


@main.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    tarefa = Tarefa.query.get(id)
    if not tarefa:
        return jsonify({"ERRO", "TAREFA NÃO ENCONTRADA"}), 404
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"MSG", "TAREFA DELETADA COM SUCESSO"}), 200


@main.route("/tasks", methods=["PUT"])
def update_task(id):
    tarefa = Tarefa.query.get_or_404(id)
    data = request.json
    try:
        tarefa.data_limite = datetime.strptime(data["data_limite"], "%d/%m/%Y").date()
    except ValueError:
        return jsonify({"erro", "DATA INVÁLIDA"}), 400

    tarefa.nome = data["nome"]
    tarefa.custo = data["custo"]

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"erro", "NOME OU ORDEM JÀ EXISTENTES"}), 400

    return jsonify({"MSG", "TAREFA ATUALIZADA COM SUCESSO"}), 200


@main.route("/tarefas/<int:id>/up", methods=["PUT"])
def up_task(id):
    tarefa = Tarefa.query.get_or_404(id)

    tarefa_acima = (
        Tarefa.query.filter(Tarefa.ordem < tarefa.ordem)
        .order_by(Tarefa.ordem.desc())
        .first()
    )

    if not tarefa_acima:
        return jsonify({"MSG", "A TAREFA JÁ ESTÁ NO TOPO"}), 400

    tarefa.ordem, tarefa_acima.ordem = tarefa_acima.ordem, tarefa.ordem
    db.session.commit()
    return jsonify({"MSG", "TAREFA MOVIDA PARA CIMA"})


@main.route("/tarefas/<int:id>/down", methods=["PUT"])
def down_task(id):
    tarefa = Tarefa.query.get_or_404(id)

    tarefa_abaixo = (
        Tarefa.query.filter(Tarefa.ordem > tarefa.ordem)
        .order_by(Tarefa.ordem.asc())
        .first()
    )
    if not tarefa_abaixo:
        return jsonify({"MSG,A TAREFA JÀ ESTÁ NA ÚLTIMA POSIÇÃO"}), 400

    tarefa.ordem, tarefa_abaixo.ordem = tarefa_abaixo.ordem, tarefa.ordem
    db.session.commit()
    return jsonify({"MSG", "TAREFA MOVIDA PARA BAIXO"})
