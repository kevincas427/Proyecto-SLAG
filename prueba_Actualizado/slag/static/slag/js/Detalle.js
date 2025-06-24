
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

document.getElementById('formulario').addEventListener('submit', function(event) {
    const selectTalla = document.getElementById('Talla');
    // Verifica si la opción seleccionada es la predeterminada (sin valor)
    if (selectTalla.selectedIndex === 0) {
        alert('Por favor, escoge una talla antes de añadir al carrito.');
        event.preventDefault(); // Evita que el formulario se envíe
    }
});
