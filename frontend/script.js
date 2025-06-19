const API_URL = "http://143.198.59.31/books"; //Nuestro droplet, API

// Para cargar libros (get)
async function getBooks() {
  const res = await fetch(API_URL);
  const data = await res.json();
  const libros = Array.isArray(data) ? data : data.books;
  const lista = document.getElementById("book-list");
  const filtro = document.getElementById("categoriaFiltro").value;

  lista.innerHTML = "";
  const categoriaTitulo = document.getElementById("tituloCategoria");
  categoriaTitulo.innerHTML = filtro ? `📚 Categoría: <strong>${filtro}</strong>` : "";
  const categorias = new Set();

  libros.forEach((libro) => {
    categorias.add(libro.category);

    if (filtro && libro.category !== filtro) return;

    const card = document.createElement("div");
    card.className = "book-card";
    card.innerHTML = `
      <h3>${libro.title}</h3>
      <p><strong>Autor:</strong> ${libro.author}</p>
      <p><strong>Año:</strong> ${libro.year}</p>
      <p><strong>Categoría:</strong> ${libro.category}</p>
      <p><strong>Páginas:</strong> ${libro.numOfPages}</p>
      <div class="card-actions">
        <button onclick="editBook(this, ${libro.code}, '${libro.title}', '${libro.author}', ${libro.year}, '${libro.category}', ${libro.numOfPages})">✏️ Editar</button>
        <button onclick="deleteBook(${libro.code})">🗑 Eliminar</button>
      </div>
    `;
    lista.appendChild(card);
  });

  // Es para rellenar los selects de categoría
  const selectFiltro = document.getElementById("categoriaFiltro");
  const selectFormulario = document.getElementById("categoria");

  selectFiltro.innerHTML = '<option value="">Todas las categorías</option>';
  selectFormulario.innerHTML = '<option value="">Selecciona una categoría</option>';

  [...categorias].forEach((cat) => {
    const optionFiltro = document.createElement("option");
    optionFiltro.value = cat;
    optionFiltro.textContent = cat;
    selectFiltro.appendChild(optionFiltro);

    const optionForm = document.createElement("option");
    optionForm.value = cat;
    optionForm.textContent = cat;
    selectFormulario.appendChild(optionForm);
  });

  const select = document.getElementById("categoriaFiltro");
  select.innerHTML = '<option value="">Todas las categorías</option>';
  [...categorias].forEach((cat) => {
    const option = document.createElement("option");
    option.value = cat;
    option.textContent = cat;
    select.appendChild(option);
  });
}

// Para agregar libro
document.getElementById("book-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = {
    title: document.getElementById("titulo").value,
    author: document.getElementById("autor").value,
    year: parseInt(document.getElementById("anio").value),
    category: document.getElementById("categoria").value,
    numOfPages: parseInt(document.getElementById("paginas").value),
  };

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (res.ok) {
    alert("Libro guardado ✅");
    document.getElementById("categoriaFiltro").value = "";
    getBooks();
    e.target.reset();
  } else {
    alert("Error al guardar ❌");
  }
});

// Para eliminar libro
async function deleteBook(id) {
  const confirmDelete = confirm("¿Estás seguro de eliminar este libro?");
  if (!confirmDelete) return;

  const res = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });

  if (res.ok) {
    alert("Libro eliminado ✅");
    getBooks();
  } else {
    alert("Error al eliminar ❌");
  }
}

// Para editar libro (modo inline)
function editBook(button, id, title, author, year, category, numOfPages) {
  const card = button.closest(".book-card");
  card.innerHTML = `
    <form onsubmit="saveEdit(event, ${id})">
      <input name="title" value="${title}" required />
      <input name="author" value="${author}" required />
      <input name="year" type="number" value="${year}" required />
      <input name="category" value="${category}" required />
      <input name="numOfPages" type="number" value="${numOfPages}" required />
      <div class="card-actions">
        <button type="submit">💾 Guardar</button>
        <button type="button" onclick="getBooks()">❌ Cancelar</button>
      </div>
    </form>
  `;
}

// Para guardar cambios
async function saveEdit(e, id) {
  e.preventDefault();
  const form = e.target;

  const data = {
    title: form.title.value,
    author: form.author.value,
    year: parseInt(form.year.value),
    category: form.category.value,
    numOfPages: parseInt(form.numOfPages.value),
  };

  const res = await fetch(`${API_URL}/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (res.ok) {
    alert("✅ Cambios guardados");
    getBooks();
  } else {
    alert("❌ Error al guardar cambios");
  }
}

async function buscarPorId() {
  const id = document.getElementById("busquedaId").value.trim();
  const lista = document.getElementById("book-list");
  const categoriaTitulo = document.getElementById("tituloCategoria");

  if (!id || isNaN(id)) {
    alert("🔎 Ingresa un ID válido");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/${id}`);

    if (!res.ok) throw new Error("Libro no encontrado");

    const libro = await res.json();
    lista.innerHTML = ""; // Limpia la lista
    categoriaTitulo.innerHTML = `🔎 Resultado para ID <strong>${id}</strong>`;

    const card = document.createElement("div");
    card.className = "book-card";
    card.innerHTML = `
      <h3>${libro.title}</h3>
      <p><strong>Autor:</strong> ${libro.author}</p>
      <p><strong>Año:</strong> ${libro.year}</p>
      <p><strong>Categoría:</strong> ${libro.category}</p>
      <p><strong>Páginas:</strong> ${libro.numOfPages}</p>
      <div class="card-actions">
        <button onclick="editBook(this, ${libro.code}, '${libro.title}', '${libro.author}', ${libro.year}, '${libro.category}', ${libro.numOfPages})">✏️ Editar</button>
        <button onclick="deleteBook(${libro.code})">🗑 Eliminar</button>
      </div>
    `;
    lista.appendChild(card);
  } catch (err) {
    alert("❌ No se encontró ningún libro con ese ID");
    categoriaTitulo.innerHTML = "";
    lista.innerHTML = "";
  }

  document.getElementById("busquedaId").value = "";
}


// Finalmente para cargar automáticamente
getBooks();
