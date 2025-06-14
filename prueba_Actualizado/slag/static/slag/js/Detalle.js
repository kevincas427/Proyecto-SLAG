
const InputCantidad = document.querySelector(".input-cantidad");
const BtonIncremento = document.getElementById("incremento");
const BtonDecremento = document.getElementById("decremento");
const Limpiar = document.querySelector(".btn-limpiar")

let valueByDefault = parseInt(InputCantidad.value) || 1;
InputCantidad.value = valueByDefault; 


BtonIncremento.addEventListener('click', () => {
    valueByDefault += 1;
    InputCantidad.value = valueByDefault;
});

BtonDecremento.addEventListener('click', () => {
    if (valueByDefault > 1) {
        valueByDefault -= 1;
        InputCantidad.value = valueByDefault;
    }
});

Limpiar.addEventListener('click', () =>{
    valueByDefault= 1
    InputCantidad.value =  valueByDefault
});


document.addEventListener("DOMContentLoaded", function (){
    const formulario = document.getElementById('formulario');
    const talla = document.getElementById('Talla');

    formulario.addEventListener("submit", function(e){
        if(talla.value == ""){
            e.preventDefault();
            alert("Porfavor esocoja una talla para poder agregar el producto al carrito");
            talla.focus();

        }
    });
});



