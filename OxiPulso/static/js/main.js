document
  .getElementById("measurementForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const form = document.getElementById("measurementForm");
    const resultDiv = document.getElementById("result");
    const submitButton = document.getElementById("submitButton");
    const measurementCard = document.getElementById("measurementCard");
    const bpmSpan = document.getElementById("bpm");
    const spo2Span = document.getElementById("spo2");

    // Cambiar el botón a estado de cargando
    submitButton.innerHTML = `
      <svg aria-hidden="true" class="inline-block w-5 h-5 mr-3 text-gray-200 animate-spin fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
          <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
      </svg>
      <span class="inline-block">Cargando...</span>
    `;
    submitButton.disabled = true;

    // Realizar la solicitud AJAX
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/mediciones/medir", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        submitButton.innerHTML = "Obtener Medición";
        submitButton.disabled = false;

        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          if (response.success) {
            bpmSpan.innerHTML = response.hr;
            spo2Span.innerHTML = response.spo2;
            form.classList.add("hidden");
            measurementCard.classList.remove("hidden");

            // Mostrar alertas dependiendo de los valores
            const bpm = response.hr;
            const spo2 = response.spo2;

            // if (bpm >= 60 && bpm <= 100 && spo2 >= 95) {
            if (bpm >= 60 && bpm <= 100) {
              Swal.fire({
                icon: "success",
                title: "Valores normales",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            } else if (
              (bpm >= 50 && bpm < 60) ||
              (bpm > 100 && bpm <= 120) 
              // (spo2 >= 90 && spo2 < 95)
            ) {
              Swal.fire({
                icon: "warning",
                title: "Precaución",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "¡Peligro!",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            }
          } else {
            const errorMessage =
              response.error || "Error al obtener el valor del sensor";
            Swal.fire({
              icon: "error",
              title: "Error",
              text: errorMessage,
            });
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error al realizar la solicitud",
          });
        }
      }
    };
    xhr.send("message=medir");
  });

  document
  .getElementById("newMeasurementButton")
  .addEventListener("click", function (event) {
    event.preventDefault();

    const values = document.querySelectorAll(".value");

    // Guardar los valores originales antes de iniciar la carga
    const originalValues = Array.from(values).map(value => value.innerHTML);

    // Cambiar valores a estado de cargando
    values.forEach(function (value) {
      value.innerHTML = `
          <svg aria-hidden="true" class="inline-block w-5 h-5 mr-3 text-gray-200 animate-spin fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
              <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
          </svg>
      `;
    });

    // Realizar la solicitud AJAX
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "mediciones/medir", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          if (response.success) {
            // Actualizar los valores de bpm y spo2 en el DOM
            const bpmSpan = document.getElementById("bpm");
            const spo2Span = document.getElementById("spo2");
            bpmSpan.innerHTML = response.hr;
            spo2Span.innerHTML = response.spo2;

            // Mostrar alertas dependiendo de los valores
            const bpm = response.hr;
            const spo2 = response.spo2;

            // if (bpm >= 60 && bpm <= 100 && spo2 >= 90) {
              if (bpm >= 60 && bpm <= 100) {
              Swal.fire({
                icon: "success",
                title: "Valores normales",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            } else if (
              (bpm >= 50 && bpm < 60) ||
              (bpm > 100 && bpm <= 120)
              // (spo2 >= 85 && spo2 < 90)
            ) {
              Swal.fire({
                icon: "warning",
                title: "Precaución",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "¡Peligro!",
                text: `BPM: ${bpm}, SpO₂: ${spo2}%`,
              });
            }
          } else {
            const errorMessage =
              response.error || "Error al obtener el valor del sensor";

            if (errorMessage === "No se detectó dedo") {
              Swal.fire({
                icon: "warning",
                title: "Sensor no detectado",
                text: "Por favor, coloque el dedo en el sensor.",
              });
            } else {
              Swal.fire({
                icon: "error",
                title: "Error",
                text: "Error al obtener el valor del sensor.",
              });
            }
            // Restaurar valores originales tras error
            values.forEach((value, index) => {
              value.innerHTML = originalValues[index];
            });
          }
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Error al realizar la solicitud",
          });
          // Restaurar valores originales tras error
          values.forEach((value, index) => {
            value.innerHTML = originalValues[index];
          });
        }
      }
    };
    xhr.send("message=medir");
  });
