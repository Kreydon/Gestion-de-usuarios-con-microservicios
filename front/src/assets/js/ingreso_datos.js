document.getElementById("myForm").addEventListener("submit", function (e) {
  const firstName = document.getElementById("primerNombre");
  const secondName = document.getElementById("segundoNombre");
  const apellidos = document.getElementById("apellidos");
  const celular = document.getElementById("celular");
  const nroDocumento = document.getElementById("noDocumento");
  const correoElectronico = document.getElementById("email");
  const foto = document.getElementById("foto");

  if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(firstName.value)) {
    alert(
      "El primer nombre no debe contener números ni caracteres especiales."
    );
    e.preventDefault();
  }

  if (secondName.value && !/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(secondName.value)) {
    alert(
      "El segundo nombre no debe contener números ni caracteres especiales."
    );
    e.preventDefault();
  }

  if (!/^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$/.test(apellidos.value)) {
    alert("Los apellidos no deben contener números ni caracteres especiales.");
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

  fetch("http://localhost:5000/create_users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST",
      "Access-Control-Allow-Headers": "Content-Type",
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
