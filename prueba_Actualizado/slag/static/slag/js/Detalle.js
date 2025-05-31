
const inputCantidad = document.querySelector(".input-cantidad");
const btonIncremento = document.getElementById("incremento");
const btonDecremento = document.getElementById("decremento");
const Limpiar = document.querySelector(".btn-limpiar")


let valueByDefault = parseInt(inputCantidad.value) || 1;
inputCantidad.value = valueByDefault; 


btonIncremento.addEventListener('click', () => {
    valueByDefault += 1;
    inputCantidad.value = valueByDefault;
});

btonDecremento.addEventListener('click', () => {
    if (valueByDefault > 1) {
        valueByDefault -= 1;
        inputCantidad.value = valueByDefault;
    }
});

Limpiar.addEventListener('click', () =>{
    valueByDefault= 1
    inputCantidad.value =  valueByDefault
})