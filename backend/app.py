from datetime import date

from app import create_app, db
from app.models import Tarefa

app = create_app()

if Tarefa.query.count() == 0:
    tarefas_exemplo = [
        Tarefa(
            nome="Planejar projeto", custo=500, data_limite=date(2026, 2, 10), ordem=1
        ),
        Tarefa(
            nome="Implementar backend",
            custo=1200,
            data_limite=date(2026, 2, 15),
            ordem=2,
        ),
        Tarefa(
            nome="Criar interface", custo=800, data_limite=date(2026, 2, 20), ordem=3
        ),
    ]

    db.session.add_all(tarefas_exemplo)
    db.session.commit()
    print("✅ Tarefas de exemplo criadas")

if __name__ == "__main__":
    app.run(debug=True)
