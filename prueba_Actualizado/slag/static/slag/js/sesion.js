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

// document.getElementById('form-sesion').addEventListener('submit', async function(e) {
//   e.preventDefault();

//   const password1 = document.getElementById('password1')
//   const password2 = document.getElementById('password2')

//   const response = await fetch('/sesion/',{
//     method : 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body : JSON.stringify({password1,password2})

//   });
//   const data = await response.json()

//   if(data.error1){
//     document.getElementById('mensaje-error').textContent = data.error1;
//   }else{
//     alert('Cuenta agregada correctamente')
//   }
// })

let = formulario = document
  .getElementById("form-sesion")
  .addEventListener("submit", async function (e) {
    const password1 = document.getElementById("password").value;
    const password2 = document.getElementById("password2").value;

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
    } else {
      form.style.cssText = `
        box-shadow: 0 0 10px rgb(128, 202, 106);
`;
    }
  });
