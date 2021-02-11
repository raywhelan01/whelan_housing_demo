// Add console.log to check to see if our code is working.
console.log("working");

// We create the tile layer that will be the background of our map.
let streets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}', {
attribution: 'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
	accessToken: API_KEY
});

// We create the tile layer that will be the background of our map.
let satelliteStreets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}', {
attribution: 'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
	accessToken: API_KEY
});

let light = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token={accessToken}', {
attribution: 'Map data © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
	maxZoom: 18,
	accessToken: API_KEY
});

// Create a base layer that holds both maps.
let baseMaps = {
  "Streets": streets,
  "Satellite": satelliteStreets,
  "Light": light
};

// Create the earthquake and tectonic plate layers for our map.
let home_values = new L.LayerGroup();

// We define an object that contains the overlays.
// This overlay will be visible all the time.
let overlays = {
  Home_Values: home_values
};

// Create the map object with a center and zoom level.
let map = L.map("mapid", {
  center: [
    39.5, -98.5
  ],
  zoom: 5,
  layers: [streets]
});


// Then we add a control to the map that will allow the user to change
// which layers are visible.
L.control.layers(baseMaps, overlays).addTo(map);

choro = d3.json("https://raw.githubusercontent.com/raywhelan01/Housing_Final_Project/Ray/Machine%20Learning/Resources/choro.json")

// the function for setting the style
function style(feature) {
    // default color is black
    let color = "#000"
    let covidis = ["#002051","#0d346b","#33486e","#575c6e","#737172","#8b8677","#a49d78","#c3b56d","#e6cf59","#fdea45"]
    // if geometry is defined, get the color from the d3 RdPu colormap
    if (feature.properties.decile !== undefined)
        color = covidis[feature.properties.decile -1];
    return {
        fillColor: color,
        color: "#000",
        weight: 1,
        fillOpacity: 0.75
    };
}

// Define a function that will get called for each geometry feature
// This will add a Popup feature for each feature
function onEachFeature(feature, layer) {

    if (feature.properties.decile !== undefined) {
        
        // value of percent no internet for this county
        // use the d3-format library: https://github.com/d3/d3-format
        let value = feature.properties.home_value;
        let formattedValue = d3.format("$.2f")(value);
        
        // define the popup content
        let content = `<div>County Name: ${feature.properties.name}</div>
                       <div>Median Home Value: ${formattedValue}</div>
                       <div>Decile: ${feature.properties.decile}</div>`

        // bind the popup to the layer
        layer.bindPopup(content);
        
        layer.on('mouseover', function (e) {
            this.openPopup();
        });
        layer.on('mouseout', function (e) {
            this.closePopup();
        });
    }
}

// add the counties to the map, with the style and popup
// See https://leafletjs.com/examples/geojson/

choro.then(function(data) {
    console.log(data);
    //Create the GeoJson data
    L.geoJSON(data, {
      style: style,
      onEachFeature: onEachFeature
      }
    ).addTo(home_values);
    home_values.addTo(map);
  });    



// Create a legend control object.
let legend = L.control({
  position: "bottomright"
});

// Then add all the details for the legend.
legend.onAdd = function() {
  let div = L.DomUtil.create("div", "info legend");

const deciles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const colors = ["#002051","#0d346b","#33486e","#575c6e","#737172","#8b8677","#a49d78","#c3b56d","#e6cf59","#fdea45"];

// Looping through our intervals to generate a label with a colored square for each interval.
for (var i = 0; i < deciles.length; i++) {
  console.log(colors[i]);
  div.innerHTML +=
    "<i style='background: " + colors[i] + "'></i> " +
    deciles[i] + "<br>";
}
return div;
};
legend.addTo(map);

