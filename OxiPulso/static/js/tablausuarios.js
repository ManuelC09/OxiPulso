let productos = []; // Variable para almacenar los datos de los productos
let productosMostrados = []; // Variable para almacenar los productos mostrados actualmente
let resultadosPorPagina = 5; // Número de productos por página
let paginaActual = 1; // Página actual de la paginación

document.addEventListener("DOMContentLoaded", function() {
  cargarDatos();
});

function cargarDatos() {
  fetch('/mediciones/historial/datos')
    .then(response => response.json())
    .then(data => {
      productos = data.mediciones; // Almacenar los datos en la variable productos
      actualizarProductosMostrados();
      mostrarProductos();
      activarPaginacion();
      activarBusqueda();
    })
    .catch(error => console.error('Error al cargar los datos:', error));
}

function mostrarProductos() {
  const tableBody = document.getElementById('tableBody');
  tableBody.innerHTML = '';

  productosMostrados.forEach(producto => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td class="px-6 py-4 whitespace-nowrap">${producto.bpm}</td>
      <td class="px-6 py-4 whitespace-nowrap">${producto.spo2}</td>
      <td class="px-6 py-4 whitespace-nowrap">${producto.hora}</td>
      <td class="px-6 py-4 whitespace-nowrap">${producto.fecha}</td>
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

  const paginacion = document.getElementById('paginacion');
  paginacion.innerHTML = '';

  for (let i = 1; i <= paginas; i++) {
    const boton = document.createElement('button');
    boton.textContent = i;
    boton.className = 'pagination-btn min-w-[2.5rem] h-[2.5rem] m-1 bg-blue-700 text-white border border-transparent ';
    if (i === paginaActual) {
      boton.classList.add('bg-blue-900');
    }
    boton.addEventListener('click', () => {
      paginaActual = i;
      actualizarProductosMostrados();
      mostrarProductos();
      actualizarBotonesPaginacion();
    });
    paginacion.appendChild(boton);
  }
}

function actualizarBotonesPaginacion() {
  const botonesPaginacion = document.querySelectorAll('.pagination-btn');
  botonesPaginacion.forEach(btn => {
    const numeroPagina = parseInt(btn.textContent);
    if (numeroPagina === paginaActual) {
      btn.classList.add('bg-blue-900');
    } else {
      btn.classList.remove('bg-blue-900');
    }
  });
}

// function activarBusqueda() {
//   const inputBusqueda = document.createElement('input');
//   inputBusqueda.setAttribute('type', 'text');
//   inputBusqueda.setAttribute('placeholder', 'Buscar...');
//   inputBusqueda.className = 'px-4 py-2 mb-4 border border-gray-300 rounded focus:outline-none focus:border-blue-500';
//   inputBusqueda.addEventListener('input', () => {
//     const valorBusqueda = inputBusqueda.value.toLowerCase().trim();
//     const productosFiltrados = productos.filter(producto =>
//       producto.bpm.toLowerCase().includes(valorBusqueda) ||
//       producto.spo2.toLowerCase().includes(valorBusqueda) ||
//       producto.hora.toLowerCase().includes(valorBusqueda) ||
//       producto.fecha.toLowerCase().includes(valorBusqueda)
//     );
//     productos = productosFiltrados; // Actualizar la lista de productos filtrados
//     paginaActual = 1; // Volver a la primera página al realizar una búsqueda
//     actualizarProductosMostrados();
//     mostrarProductos();
//     activarPaginacion();
//   });

//   const contenedor = document.querySelector('.tabla-scroll');
//   contenedor.insertBefore(inputBusqueda, contenedor.firstChild);
// }

function ordenarColumna(index) {
  const tipoDato = typeof productos[0][Object.keys(productos[0])[index]];

  productos.sort((a, b) => {
    let valorA = a[Object.keys(a)[index]];
    let valorB = b[Object.keys(b)[index]];

    if (tipoDato === 'string') {
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