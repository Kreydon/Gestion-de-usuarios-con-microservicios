const createButton = document.getElementById("create");
const readButton = document.getElementById("read");
const updateButton = document.getElementById("update");
const deleteButton = document.getElementById("delete");
const cerrarBtn = document.getElementById("cerrar");
let popupTitle = "";
let btnAccion = "";

createButton.addEventListener("click", function () {
  window.location.href = "ingreso_datos.html";
});

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
      });
  } else if (btnAccion === "Actualizar usuario") {
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
          window.location.href = `actualizar_datos.html?noDocumento=${noDocumento}`;
        }
      })
      .catch((error) => {
        // Capturar y manejar cualquier error que ocurra durante la solicitud
        console.error("Error en la solicitud:", error);
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
        if (!response.ok) {
          throw new Error(
            `Error en la solicitud: ${response.status} ${response.statusText}`
          );
        }
        return response.json();
      })
      .then((data) => {
        console.log(data); // Manejar la respuesta del servidor, si es necesario
      })
      .catch((error) => {
        // Capturar y manejar cualquier error que ocurra durante la solicitud
        console.error("Error en la solicitud:", error);
      });
  }
});
