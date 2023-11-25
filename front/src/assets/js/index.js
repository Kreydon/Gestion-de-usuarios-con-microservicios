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
  // Dependiendo de la acción, redirigir a la página correspondiente
  if (btnAccion === "Consultar usuario") {
    window.location.href = "consultar_datos.html";
  } else if (btnAccion === "Actualizar usuario") {
    window.location.href = "actualizar_datos.html";
  } // Agrega más casos según tus necesidades
});
