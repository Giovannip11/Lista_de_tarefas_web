# 📝 Gerenciador de Tarefas

Aplicação web para gerenciamento de tarefas, permitindo criar, editar, excluir e ordenar tarefas, com persistência em banco de dados e acesso via navegador, sem necessidade de instalação local.

O sistema foi desenvolvido,seguindo requisitos funcionais específicos e boas práticas de separação entre front-end e back-end.

---

## 🚀 Funcionalidades

- 📋 Listagem de tarefas em ordem definida pelo campo **ordem de apresentação**
- ➕ Inclusão de novas tarefas
- ✏️ Edição de tarefas existentes
- 🗑️ Exclusão de tarefas
- 🔼🔽 Reordenação dinâmica das tarefas (subir/descer)
- 💰 Destaque visual para tarefas com custo **≥ R$ 1.000,00**
- 📊 Exibição do **somatório total dos custos**
- ⚠️ Validação de dados (não permite valores negativos)
- 🌐 Aplicação acessível via navegador (sem instalação)

---

## 🛠️ Tecnologias Utilizadas

### Back-end
- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- PostgreSQL
- Gunicorn

### Front-end
- HTML5
- CSS3
- JavaScript (Fetch API)

### Deploy
- **Back-end:** Render
- **Front-end:** Vercel

---

## 🗂️ Estrutura do Projeto

```text
Lista_de_tarefas/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── app.py
│   ├── start.sh
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
