const container = document.querySelector(".container");
const btnsignin = document.getElementById("btn-sign-in");
const btnsignup = document.getElementById("btn-sign-up");
const Contrasena = document.getElementById("contrasena");
const mensaje = document.getElementById("mensaje")
const fotmulario = document.getElementById("registro")

btnsignin.addEventListener("click",()=>{
    container.classList.remove("toggle");
});
btnsignup.addEventListener("click",()=>{
    container.classList.add("toggle");
});