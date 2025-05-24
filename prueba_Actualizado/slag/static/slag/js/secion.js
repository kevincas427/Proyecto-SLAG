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
  .getElementById("registroForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const password = document.getElementsById("password1").value;
    const password2 = document.getElementsById("password2").value;
    const error = document.getElementsById("error").value;

    if (password.lengh < 10) {
      error.textContent = "La contraseña debe tener almenos 10 digitos";
      return;
    }
    if (!/[A-Z]/.test(password)) {
        error.textContent = "La contraseña debe tener por lo menos una mayuscula";
        return;
    };
    if (!/[0-9]/.test(password)){
        error.textContent = "La contraseña debe tener por lo menos un numero";
        return;
    }
    if (password != password2){
        error.textContent = "Las contraseñas deben de coincidir"
    }
  });
