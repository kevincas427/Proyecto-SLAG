document
  .getElementById("formulario")
  .addEventListener("submit", function (e) {
    const new_password = document.getElementById('password').value;

    if (new_password.length < 10 || !/[A-Z]/.test(new_password)) {
      e.preventDefault();
      alert("la contraseña debe tener almenos 10 caracteres y una mayuscula");
      return;
    } else if (!/[0-9]/.test(new_password) || !/[^A-Za-z0-9]/.test(new_password)) {
      e.preventDefault();
      alert("La contraseña debe tener almenos un simbolo y un numero");
      return;
    } else {
      alert("Contraseña actualizada con exito");
    }
  });
