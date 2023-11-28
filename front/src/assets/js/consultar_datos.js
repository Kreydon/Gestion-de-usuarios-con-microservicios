const urlParams = new URLSearchParams(window.location.search);
const noDoc = urlParams.get("noDocumento");
console.log(noDoc);

window.addEventListener("load", async function () {
  fetch(`http://localhost:5001/read_users/${noDoc}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const dateB = new Date(data.fechaNacimiento);
      console.log(data.fechaNacimiento);
      const year = dateB.getFullYear();
      const month = (dateB.getMonth() + 1).toString().padStart(2, "0");
      const day = (dateB.getDate() + 1).toString().padStart(2, "0");
      const formatted = `${year}-${month}-${day}`;

      console.log(formatted);
      document.getElementById("tipoDocumento").value = data.tipoDocumento;
      document.getElementById("nroDocumento").value = data.noDocumento;
      document.getElementById("primerNombre").value = data.firstName;
      document.getElementById("segundoNombre").value = data.secondName || "";
      document.getElementById("apellidos").value = data.apellidos;
      document.getElementById("fechaNacimiento").value = formatted;
      console.log(document.getElementById("fechaNacimiento").value);
      document.getElementById("genero").value = data.genero;
      document.getElementById("email").value = data.correoElectronico;
      document.getElementById("celular").value = data.celular;
      document.getElementById("foto").value = data.foto;
    })
    .catch((error) => console.error("Error:", error));
  const myForm = document.getElementById("myForm");

  const data = {};

  for (let element of myForm.elements) {
    if (element.name) {
      data[element.name] = element.value;
    }
  }

  // data tendrá los valores del formulario
  console.log(data);

  fetch("http://localhost:5001/logs", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      // Manejar la respuesta del servidor
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
