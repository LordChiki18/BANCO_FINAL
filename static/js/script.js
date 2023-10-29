
var valorOriginalCtte = "";

function ocultarMontoCtte() {
  var btnCuentaCtte = document.getElementById("hideAmountCtte");
  var montoCuentaCtte = document.getElementById("amountCtte");

  if (btnCuentaCtte.textContent === "Ocultar monto") {
    valorOriginalCtte = montoCuentaCtte.textContent; // Guardo el valor original
    var asteriscos = "********";
    montoCuentaCtte.textContent = asteriscos;
    btnCuentaCtte.textContent = "Mostrar monto";
  } else {
    montoCuentaCtte.textContent = valorOriginalCtte;
    btnCuentaCtte.textContent = "Ocultar monto";
  }
}

var valorOriginalCaja = "";

function ocultarMontoCaja() {
  var btnCuentaCaja = document.getElementById("hideAmountCaja");
  var montoCuentaCaja = document.getElementById("amountCaja");

  if (btnCuentaCaja.textContent === "Ocultar monto") {
    valorOriginalCaja = montoCuentaCaja.textContent; // Guardo el valor original
    var asteriscos = "********";
    montoCuentaCaja.textContent = asteriscos;
    btnCuentaCaja.textContent = "Mostrar monto";
  } else {
    montoCuentaCaja.textContent = valorOriginalCaja;
    btnCuentaCaja.textContent = "Ocultar monto";
  }
}

