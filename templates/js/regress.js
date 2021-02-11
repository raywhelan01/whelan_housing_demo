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

// Reference the HTML table using d3
var tbody = d3.select("tbody");
//Function for creating the table 
function buildTable(fips) {
    let vars = ['NAME', '% Housing Units Occupied', '% Unemployment Rate', '% Born in State', 'Median Income', 'Median Home Value'];
    tbody.html("");
    d3.json("https://raw.githubusercontent.com/raywhelan01/Housing_Final_Project/Ray/Machine%20Learning/Resources/county.json").then(function(data) {
      console.log(data);
      let row = tbody.append("tr");
      vars.forEach((val) => {
          let cell = row.append("td");
          cell.text(data[fips][val]);

      });
      let hypo = data[fips];
      hypo['% Housing Units Occupied'] = data[fips]['% Housing Units Occupied']*(1+(occSlide.value/100));
      hypo['% Unemployment Rate'] = data[fips]['% Unemployment Rate']*(1+(empSlide.value/100));
      hypo['% Born in State'] = data[fips]['% Born in State']*(1+(stateSlide.value/100));
      hypo['Median Income'] = data[fips]['Median Income']*(1+(incSlide.value/100));
      let row2 = tbody.append("tr");
      vars.forEach((val) => {
          let cell2 = row2.append("td");
          cell2.text(hypo[val]);
      });
    })
}

function predict() {
  let fips =  d3.select("#fips").property("value");
  console.log(fips);
  buildTable(fips);
}

d3.selectAll("#predict-btn").on("click", predict);

buildTable('6081.0');





