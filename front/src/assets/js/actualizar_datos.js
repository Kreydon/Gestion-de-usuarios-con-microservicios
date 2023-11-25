const templateHTML = `
<header>
<h1>Formulario de Actualización</h1>
</header>
<main>
<div class="flex-container">
  <form id="myForm" enctype="multipart/form-data">
    <div class="flex-container2">
      <div class="izquierda"><label for="tipoDocumento">Tipo de Documento:</label>
        <select class="select" id="tipoDocumento" name="tipoDocumento">
          <option value="Tarjeta de identidad">Tarjeta de Identidad</option>
          <option value="Cédula">Cédula</option>
        </select><br>

        <label for="nroDocumento">Nro. Documento:</label>
        <input type="text" id="nroDocumento" name="nroDocumento" value="123456"
          title="Máximo 10 números, solo se permiten carácteres númericos." required pattern="[0-9]{1,10}" readonly><br>

        <label for="primerNombre">Primer Nombre:</label>
        <input type="text" id="primerNombre" name="primerNombre" value="primerNombre"
          title="Máximo 30 carácteres, solo se permiten carácteres alfabeticos." required maxlength="30"
          pattern="[A-Za-záéíóúÁÉÍÓÚñÑ\s]+"><br>

        <label for="segundoNombre">Segundo Nombre:</label>
        <input type="text" id="segundoNombre" name="segundoNombre" value="segundoNombre"
          title="Máximo 30 carácteres, solo se permiten carácteres alfabeticos." maxlength="30"
          pattern="[A-Za-záéíóúÁÉÍÓÚñÑ\s]+"><br>

        <label for="apellidos">Apellidos:</label>
        <input type="text" id="apellidos" name="apellidos" value="apellidos"
          title="Máximo 60 carácteres, solo se permiten carácteres alfabeticos." required maxlength="60"
          pattern="[A-Za-záéíóúÁÉÍÓÚñÑ\s]+"><br>

        <label for="fechaNacimiento">Fecha de Nacimiento:</label>
        <input type="date" id="fechaNacimiento" name="fechaNacimiento" value="2023-11-24" readonly required><br>

        <label for="genero">Género:</label>
        <select class="select" id="genero" name="genero">
          <option value="Masculino">Masculino</option>
          <option value="Femenino">Femenino</option>
          <option value="No binario">No binario</option>
          <option value="Prefiero no reportar">Prefiero no reportar</option>
        </select><br>

        <label for="email">Correo Electrónico:</label>
        <input type="email" id="email" name="email" value="email"
          title="Se requiere un formato tipo email. Ejemplo: example@ejemplo.com" required><br>

        <label for="celular">Celular:</label>
        <input type="tel" id="celular" name="celular" value="123456"
          title="Máximo 10 números, solo se permiten carácteres númericos." required pattern="[0-9]{10}"><br>
      </div>
      <div class="derecha">
        <img id="imagen-persona" src="public/default_image.jpeg" alt="Imagen">
        <div class="img-content">
          <label for="foto">Foto:</label>
          <input type="file" id="foto" name="foto" accept=".jpg, .jpeg, .png" required><br>
        </div>
      </div>
    </div>
    <input type="submit" value="Enviar">
  </form>
</div>
</main>
`;

document.getElementById("app").innerHTML = templateHTML;
