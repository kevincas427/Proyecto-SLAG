const inputCantidad = document.querySelector(".input-cantidad")
const btonIncremento = document.getElementById("incremento");
const btonDecremento = document.getElementById("decremento")

let valueByDefault = parseInt(inputCantidad.value)
console.log("Probando si agarra js desde django")
alert("Probando si agarra js desde django")
//Funciones CLick

btonIncremento.addEventListener('click',() =>{
    valueByDefault += 1
    inputCantidad.value = valueByDefault
})
btonDecremento.addEventListener('click',() =>{
    valueByDefault -= 1
    inputCantidad.value = valueByDefault
})