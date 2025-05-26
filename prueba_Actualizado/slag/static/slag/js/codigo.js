document
  .getElementsByid("formulario")
  .addEventListener('submit', async function (e) {
    const password = document.getElementById("password");

    if (password.length < 8) {
      alert("La contraseña debe de tener almenos 8 caracteres");
      e.preventDefault();
      return
    } else if (!/[A-Z]/.test(password)) {
        alert("La contraseña debe tener al menos una mayusacula");
        e.preventDefault();
        return
    } else if (!/[0-9]/.test(password) || !/[^A-Za-z0-9]/.test(password)) {
        e.preventDefault();
        alert("La contraseña debe tener almenos un simbolo y un numero");
        return
    } else {
        alert('Contraseña actualizada con exito')
    }
  });
