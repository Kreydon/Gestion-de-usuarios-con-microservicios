const urlParams = new URLSearchParams(window.location.search);
const noDoc = urlParams.get("noDocumento");

window.addEventListener("load", async function () {
  fetch(`http://localhost:5000/read_users/${noDoc}`)
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

      document.getElementById("tipoDocumento").value = data.tipoDocumento;
      document.getElementById("noDocumento").value = data.noDocumento;
      document.getElementById("primerNombre").value = data.firstName;
      document.getElementById("segundoNombre").value = data.secondName || "";
      document.getElementById("apellidos").value = data.apellidos;
      document.getElementById("fechaNacimiento").value = formatted;
      document.getElementById("genero").value = data.genero;
      document.getElementById("email").value = data.correoElectronico;
      document.getElementById("celular").value = data.celular;
      document.getElementById("foto").value = data.foto;
    })
    .catch((error) => console.error("Error:", error));

  document.getElementById("myForm").addEventListener("submit", function (e) {
    const firstName = document.getElementById("primerNombre");
    const secondName = document.getElementById("segundoNombre");
    const apellidos = document.getElementById("apellidos");
    const celular = document.getElementById("celular");
    const nroDocumento = document.getElementById("noDocumento");
    const correoElectronico = document.getElementById("email");
    const foto = document.getElementById("foto");

    console.log(nroDocumento.value);

    if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(firstName.value)) {
      alert(
        "El primer nombre no debe contener números ni caracteres especiales."
      );
      e.preventDefault();
    }

    if (
      secondName.value &&
      !/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(secondName.value)
    ) {
      alert(
        "El segundo nombre no debe contener números ni caracteres especiales."
      );
      e.preventDefault();
    }

    if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(apellidos.value)) {
      alert(
        "Los apellidos no deben contener números ni caracteres especiales."
      );
      e.preventDefault();
    }

    if (!/^\d{10}$/.test(celular.value)) {
      alert("El número de celular debe contener 10 dígitos numéricos.");
      e.preventDefault();
    }

    if (!/^\d{1,10}$/.test(nroDocumento.value)) {
      alert("El número de documento debe contener solo dígitos numéricos.");
      e.preventDefault();
    }

    if (foto.files.length > 0 && foto.files[0].size > 2 * 1024 * 1024) {
      alert("El tamaño de la foto no debe superar 2 MB.");
      e.preventDefault();
    }

    e.preventDefault();

    const formData = new FormData(this);

    foto.addEventListener("change", handleFileSelect);

    function handleFileSelect(event) {
      const selectedFile = event.target.files[0];

      if (selectedFile) {
        // Leer el contenido del archivo usando FileReader
        const reader = new FileReader();

        reader.onload = function (e) {
          // e.target.result contiene el contenido del archivo en formato Base64
          const imageBase64 = e.target.result;
          foto.value = imageBase64;
        };

        // Leer como un URL de datos (Base64)
        reader.readAsDataURL(selectedFile);
      }
    }

    fetch(`http://localhost:5000/update_users/${noDoc}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(Object.fromEntries(formData)),
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

  document.getElementById("foto").addEventListener("change", function (e) {
    const imagenSubida = document.getElementById("imagen-persona");
    const archivo = e.target.files[0]; // Obtiene el primer archivo seleccionado

    if (archivo) {
      // Verifica que se haya seleccionado un archivo
      const reader = new FileReader();

      reader.onload = function (e) {
        // Actualiza la fuente de la imagen con la imagen cargada
        imagenSubida.src = e.target.result;
      };

      // Lee el archivo como una URL de datos (base64)
      reader.readAsDataURL(archivo);
    } else {
      // Si no se selecciona un archivo, puedes restaurar la imagen predeterminada
      imagenSubida.src = "public/default_image.jpeg";
    }
  });
});
