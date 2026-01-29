const API = "https://lista-de-tarefas-web.onrender.com";
let editId = null;
let deleteId = null;

async function loadTasks(showLoading = true) {
  if (showLoading) {
    document.getElementById("loading").style.display = "flex";
  }

  try {
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
          <button onclick="openDeleteModal(${t.id})">🗑️</button>
        </td>
      `;

      tbody.appendChild(tr);
    });

    document.getElementById("total").innerText =
      `Total: R$ ${total.toFixed(2)}`;
  } catch (err) {
    document.getElementById("list").innerHTML =
      `<tr><td colspan="4">Erro ao carregar tarefas</td></tr>`;
  } finally {
    if (showLoading) {
      document.getElementById("loading").style.display = "none";
    }
  }
}

async function addTask() {
  const nome = document.getElementById("nome").value;
  const custo = document.getElementById("custo").value;
  const data = document.getElementById("data").value;

  if (!nome || !custo || !data) {
    alert("Preencha todos os campos");
    return;
  }
  if (custo < 0) {
    showError("O custo não pode ser negativo");
    return;
  }

  const res = await fetch(`${API}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome,
      custo,
      data_limite: data.split("-").reverse().join("/"),
    }),
  });

  const dataRes = await res.json();

  if (!res.ok) {
    showError(dataRes.erro || "Erro ao criar tarefa");
    return;
  }

  loadTasks();
}

async function moveUp(id) {
  await fetch(`${API}/tasks/${id}/up`, { method: "PUT" });
  loadTasks(false);
}

async function moveDown(id) {
  await fetch(`${API}/tasks/${id}/down`, { method: "PUT" });
  loadTasks(false);
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

  if (!nome || !data || custo < 0) {
    showError("Preencha todos os campos e o custo não pode ser negativo");
    return;
  }
  if (custo < 0) {
    showError("O custo não pode ser negativo");
    return;
  }

  const res = await fetch(`${API}/tasks/${editId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome,
      custo,
      data_limite: data.split("-").reverse().join("/"),
    }),
  });

  const dataRes = await res.json();

  if (!res.ok) {
    showError(dataRes.erro || "Erro ao editar tarefa");
    return;
  }

  closeModal();
  loadTasks();
}

loadTasks();
function openDeleteModal(id) {
  deleteId = id;
  document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
  document.getElementById("deleteModal").style.display = "none";
  deleteId = null;
}

async function confirmDelete() {
  if (!deleteId) return;

  await fetch(`${API}/tasks/${deleteId}`, {
    method: "DELETE",
  });

  closeDeleteModal();
  loadTasks();
}
function showError(msg) {
  document.getElementById("errorMessage").innerText = msg;
  document.getElementById("errorModal").style.display = "block";
}

function closeErrorModal() {
  document.getElementById("errorModal").style.display = "none";
}
