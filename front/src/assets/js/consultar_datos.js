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
      const year = dateB.getFullYear();
      const month = dateB.getMonth() + 1;
      const day = dateB.getDate();
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
});
