const createButton = document.getElementById("create");
const readButton = document.getElementById("read");
const updateButton = document.getElementById("update");
const deleteButton = document.getElementById("delete");
const cerrarBtn = document.getElementById("cerrar");
let popupTitle = "";
let btnAccion = "";

createButton.addEventListener("click", function () {
  fetch("http://localhost:5000/create_users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      window.location.href = "ingreso_datos.html";
    })
    .catch((error) => {
      console.error("Error:", error);
      if (
        error instanceof TypeError &&
        error.message.includes("NetworkError")
      ) {
        window.location.href = "servicio_apagado.html";
      }
    });
});

const showLogsButton = document.getElementById("showLogs");

showLogsButton.addEventListener("click", function () {
  fetch('http://localhost:5000/logs')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(logs => {
      createLogsPopup(logs);
    })
    .catch(e => {
      console.error('Error al obtener los logs:', e);
    });
});

function createLogsPopup(logs) {
  const popup = document.createElement('div');
  popup.classList.add('popup');
  popup.innerHTML = '<h2>Logs de Registro</h2><div class="logs-container"></div><button class="close-btn">Cerrar</button>';

  const logsContainer = popup.querySelector('.logs-container');
  logs.forEach(log => {
    const logEntry = document.createElement('p');
    logEntry.textContent = `Documento: ${log.noDocumento}, Usuario: ${log.usuario}, Acción: ${log.accion}, Fecha: ${log.fechaAccion}`;
    logsContainer.appendChild(logEntry);
  });
  const closeBtn = popup.querySelector('.close-btn');
  closeBtn.addEventListener('click', () => {
    document.body.removeChild(popup);
  });

  document.body.appendChild(popup);
}
// FIN BOTÓN LOGS

readButton.addEventListener("click", function () {
  popupTitle = "Ingrese el documento del usuario que desee consultar: ";
  btnAccion = "Consultar usuario";
  openPopup();
});

updateButton.addEventListener("click", function () {
  popupTitle = "Ingrese el documento del usuario que desee actualizar: ";
  btnAccion = "Actualizar usuario";
  openPopup();
});

deleteButton.addEventListener("click", function () {
  popupTitle = "Ingrese el documento del usuario que desee eliminar: ";
  btnAccion = "Eliminar usuario";
  openPopup();
});

cerrarBtn.addEventListener("click", function () {
  document.getElementById("popup").style.display = "none";
});

function openPopup() {
  document.getElementById("popup").style.display = "flex";
  document.querySelector(".popup p").innerText = popupTitle;
  document.querySelector(".popup #accion").innerText = btnAccion;
}

document.querySelector(".popup #accion").addEventListener("click", function () {
  if (btnAccion === "Consultar usuario") {
    const noDocumento = document.getElementById("userID").value;

    // Realizar la solicitud a la API
    fetch(`http://localhost:5001/read_users/${noDocumento}`)
      .then((response) => {
        // Verificar si la respuesta fue exitosa (código de estado en el rango 200-299)
        if (!response.ok) {
          throw new Error(
            `Error en la solicitud: ${response.status} ${response.statusText}`
          );
        }
        return response.json();
      })
      .then((data) => {
        // Verificar si se encontró el usuario
        if (data.mensaje && data.mensaje === "Usuario no encontrado") {
          console.log("Usuario no encontrado");
        } else {
          // Redirigir a la página de consulta_usuario.html
          window.location.href = `consultar_datos.html?noDocumento=${noDocumento}`;
        }
      })
      .catch((error) => {
        // Capturar y manejar cualquier error que ocurra durante la solicitud
        console.error("Error en la solicitud:", error);
        if (
          error instanceof TypeError &&
          error.message.includes("NetworkError")
        ) {
          window.location.href = "servicio_apagado.html";
        }
      });
  } else if (btnAccion === "Actualizar usuario") {
    const noDocumento = document.getElementById("userID").value;

    // Realizar la solicitud a la API
    fetch(`http://localhost:5002/read_users/${noDocumento}`)
      .then((response) => {
        // Verificar si la respuesta fue exitosa (código de estado en el rango 200-299)
        if (!response.ok) {
          throw new Error(
            `Error en la solicitud: ${response.status} ${response.statusText}`
          );
        }
        return response.json();
      })
      .then((data) => {
        // Verificar si se encontró el usuario
        if (data.mensaje && data.mensaje === "Usuario no encontrado") {
          console.log("Usuario no encontrado");
        } else {
          // Redirigir a la página de consulta_usuario.html
          window.location.href = `actualizar_datos.html?noDocumento=${noDocumento}`;
        }
      })
      .catch((error) => {
        // Capturar y manejar cualquier error que ocurra durante la solicitud
        console.error("Error en la solicitud:", error);
        if (
          error instanceof TypeError &&
          error.message.includes("NetworkError")
        ) {
          window.location.href = "servicio_apagado.html";
        }
      });
  } else if (btnAccion === "Eliminar usuario") {
    const noDocumento = document.getElementById("userID").value;

    fetch(`http://localhost:5003/delete_users/${noDocumento}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ noDocumento: noDocumento }),
    })
      .then((response) => {
        // Verificar si la respuesta fue exitosa (código de estado en el rango 200-299)
        if (!response.ok && response.status === 0) {
          throw new Error("Error de conexión con la API");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data); // Manejar la respuesta del servidor, si es necesario
      })
      .catch((error) => {
        console.error("Error en la solicitud:", error);
        if (
          error instanceof TypeError &&
          error.message.includes("NetworkError")
        ) {
          window.location.href = "servicio_apagado.html";
        }
      });

    fetch(`http://localhost:5003/logs/${noDocumento}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ noDocumento: noDocumento }),
    })
      .then((response) => {
        // Verificar si la respuesta fue exitosa (código de estado en el rango 200-299)
        if (!response.ok) {
          throw new Error(
            `Error en la solicitud: ${response.status} ${response.statusText}`
          );
        }
        return response.json();
      })
      .then((data) => {
        // Manejar la respuesta del servidor
        console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
