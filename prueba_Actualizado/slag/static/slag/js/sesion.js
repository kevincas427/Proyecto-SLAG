const container = document.querySelector(".container");
const btnsignin = document.getElementById("btn-sign-in");
const btnsignup = document.getElementById("btn-sign-up");
const Contrasena = document.getElementById("contrasena");
const mensaje = document.getElementById("mensaje");
const fotmulario = document.getElementById("registro");

btnsignin.addEventListener("click", () => {
  container.classList.remove("toggle");
});
btnsignup.addEventListener("click", () => {
  container.classList.add("toggle");
});

document
  .getElementById("form-sesion")
  .addEventListener("submit", async function (e) {
    const password1 = document.getElementById("password").value;
    const password2 = document.getElementById("password2").value;
    const error = document.getElementById("error").value;

    if (error == "El usuario ya existe")
      alert("EL usuario Con Este Email ya corresponde a una cuenta");

    if (password1 != password2) {
      e.preventDefault();
      alert("las contraseñas deben de ser iguales");
      return;
    } else if (password1.length < 10 || !/[A-Z]/.test(password1)) {
      e.preventDefault();
      alert("la contraseña debe tener almenos 10 caracteres y una mayuscula");
      return;
    } else if (!/[0-9]/.test(password1) || !/[^A-Za-z0-9]/.test(password1)) {
      e.preventDefault();
      alert("La contraseña debe tener almenos un simbolo y un numero");
    }
  });


  window.addEventListener('DOMContentLoaded',() => {
    const error = document.getElementById('mensage-error2');
    const mensaje = error.dataset.error;

    if (mensaje){
      alert('El Correo ya se encuentra vinculado a una cuenta existente');
      error.style.display = "block";
    }
  });