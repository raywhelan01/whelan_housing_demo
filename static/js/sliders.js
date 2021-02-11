var occSlide = document.getElementById("occup");
var occOut = document.getElementById("occupOut");
occOut.innerHTML = occSlide.value;

occSlide.oninput = function() {
  occOut.innerHTML = this.value;
}

var empSlide = document.getElementById("unemp");
var empOut = document.getElementById("unempOut");
empOut.innerHTML = empSlide.value;

empSlide.oninput = function() {
  empOut.innerHTML = this.value;
}

var stateSlide = document.getElementById("inState");
var stateOut = document.getElementById("inStateOut");
stateOut.innerHTML = stateSlide.value;

stateSlide.oninput = function() {
  stateOut.innerHTML = this.value;
}

var incSlide = document.getElementById("medInc");
var incOut = document.getElementById("medIncOut");
incOut.innerHTML = incSlide.value;

incSlide.oninput = function() {
  incOut.innerHTML = this.value;
}
