document.addEventListener("DOMContentLoaded", function () {
  cargarDatos();
});

let productos = [];
let productosMostrados = [];
let resultadosPorPagina = 5;
let paginaActual = 1;

function cargarDatos() {
  fetch("/administrador/usuarios")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      productos = data.usuarios;
      actualizarProductosMostrados();
      mostrarProductos();
      activarPaginacion();
    })
    .catch((error) => console.error("Error al cargar los datos:", error));
}

function mostrarProductos() {
  const tableBody = document.getElementById("tableBodyuser");
  tableBody.innerHTML = "";

  productosMostrados.forEach((producto) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">${producto.nombre}</td>
            <td class="px-6 py-4 whitespace-nowrap">${producto.correo}</td>
            <td class="px-6 py-4 whitespace-nowrap">${producto.nacimiento}</td>
            <td class="px-6 py-4 whitespace-nowrap">${producto.sexo}</td>
            <td class="px-6 py-4 whitespace-nowrap ">
                <a href="/administrador/descargar_datos_usuario/${producto.id}" class="group">
                    <svg class="w-4 h-4 inline-block ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="green" viewBox="0 0 24 24">
                        <path d="M12 16.5l-6-6h4V3h4v7.5h4l-6 6zm-6 1.5h12v2H6v-2z"/>
                    </svg>
                </a>
            </td>


            
        `;
    tableBody.appendChild(row);
  });
}

function actualizarProductosMostrados() {
  const inicio = (paginaActual - 1) * resultadosPorPagina;
  const fin = inicio + resultadosPorPagina;
  productosMostrados = productos.slice(inicio, fin);
}

function activarPaginacion() {
  const paginas = Math.ceil(productos.length / resultadosPorPagina);
  const paginacion = document.getElementById("paginacion");
  paginacion.innerHTML = "";

  for (let i = 1; i <= paginas; i++) {
    const boton = document.createElement("button");
    boton.textContent = i;
    boton.className =
      "pagination-btn min-w-[2.5rem] h-[2.5rem] m-1 bg-blue-700 text-white border border-transparent ";
    if (i === paginaActual) {
      boton.classList.add("bg-blue-900");
    }
    boton.addEventListener("click", () => {
      paginaActual = i;
      actualizarProductosMostrados();
      mostrarProductos();
      actualizarBotonesPaginacion();
    });
    paginacion.appendChild(boton);
  }
}

function actualizarBotonesPaginacion() {
  const botonesPaginacion = document.querySelectorAll(".pagination-btn");
  botonesPaginacion.forEach((btn) => {
    const numeroPagina = parseInt(btn.textContent);
    if (numeroPagina === paginaActual) {
      btn.classList.add("bg-blue-900");
    } else {
      btn.classList.remove("bg-blue-900");
    }
  });
}

function activarBusqueda() {
  const inputBusqueda = document.createElement("input");
  inputBusqueda.setAttribute("type", "text");
  inputBusqueda.setAttribute("placeholder", "Buscar...");
  inputBusqueda.className =
    "px-4 py-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-blue-500";
  inputBusqueda.addEventListener("input", () => {
    const valorBusqueda = inputBusqueda.value.toLowerCase().trim();
    const productosFiltrados = productos.filter(
      (producto) =>
        producto.nombre.toLowerCase().includes(valorBusqueda) ||
        producto.bpm.toString().includes(valorBusqueda) ||
        producto.spo2.toString().includes(valorBusqueda) ||
        producto.fecha.includes(valorBusqueda)
    );
    productos = productosFiltrados;
    paginaActual = 1;
    actualizarProductosMostrados();
    mostrarProductos();
    activarPaginacion();
  });

  const contenedor = document.querySelector(".tabla-scroll");
  contenedor.insertBefore(inputBusqueda, contenedor.firstChild);
}

function ordenarColumna(index) {
  const tipoDato = typeof productos[0][Object.keys(productos[0])[index]];

  productos.sort((a, b) => {
    let valorA = a[Object.keys(a)[index]];
    let valorB = b[Object.keys(b)[index]];

    if (tipoDato === "string") {
      valorA = valorA.toLowerCase();
      valorB = valorB.toLowerCase();
    }

    if (valorA < valorB) return -1;
    if (valorA > valorB) return 1;
    return 0;
  });

  actualizarProductosMostrados();
  mostrarProductos();
  activarPaginacion();
}
