const API = "http://localhost:5000";
let editId = null;

async function loadTasks() {
  const res = await fetch(`${API}/tasks`);
  const tasks = await res.json();

  const tbody = document.getElementById("list");
  tbody.innerHTML = "";

  let total = 0;

  tasks.forEach((t, index) => {
    total += Number(t.custo);

    const tr = document.createElement("tr");

    if (t.custo >= 1000) {
      tr.classList.add("destaque");
    }

    tr.innerHTML = `
      <td>${t.nome}</td>
      <td>R$ ${Number(t.custo).toFixed(2)}</td>
      <td>${t.data_limite}</td>
      <td>
        <button onclick="moveUp(${t.id})" ${index === 0 ? "disabled" : ""}>🔼</button>
        <button onclick="moveDown(${t.id})" ${index === tasks.length - 1 ? "disabled" : ""}>🔽</button>
        <button onclick='openModal(${JSON.stringify(t)})'>✏️</button>
        <button onclick="deleteTask(${t.id})">🗑️</button>
      </td>
    `;

    tbody.appendChild(tr);
  });

  document.getElementById("total").innerText = `Total: R$ ${total.toFixed(2)}`;
}

async function addTask() {
  const nome = document.getElementById("nome").value;
  const custo = document.getElementById("custo").value;
  const data = document.getElementById("data").value;

  if (!nome || !custo || !data) {
    alert("Preencha todos os campos");
    return;
  }

  await fetch(`${API}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome,
      custo,
      data_limite: data.split("-").reverse().join("/"),
    }),
  });

  document.getElementById("nome").value = "";
  document.getElementById("custo").value = "";
  document.getElementById("data").value = "";

  loadTasks();
}

async function deleteTask(id) {
  if (!confirm("Deseja realmente excluir esta tarefa?")) return;

  await fetch(`${API}/tasks/${id}`, { method: "DELETE" });
  loadTasks();
}

async function moveUp(id) {
  await fetch(`${API}/tarefas/${id}/up`, { method: "PUT" });
  loadTasks();
}

async function moveDown(id) {
  await fetch(`${API}/tarefas/${id}/down`, { method: "PUT" });
  loadTasks();
}

/* MODAL */
function openModal(task) {
  editId = task.id;

  document.getElementById("editNome").value = task.nome;
  document.getElementById("editCusto").value = task.custo;
  document.getElementById("editData").value = task.data_limite
    .split("/")
    .reverse()
    .join("-");

  document.getElementById("modal").style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
  editId = null;
}

async function saveEdit() {
  const nome = document.getElementById("editNome").value;
  const custo = document.getElementById("editCusto").value;
  const data = document.getElementById("editData").value;

  await fetch(`${API}/tasks/${editId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome,
      custo,
      data_limite: data.split("-").reverse().join("/"),
    }),
  });

  closeModal();
  loadTasks();
}

loadTasks();
