// import the data from data.js
const tableData = data;
// Reference the HTML table using d3
var tbody = d3.select("tbody");
//Function for creating the table 
function buildTable(data) {
    tbody.html("");
    data.forEach((dataRow) => {
        let row = tbody.append("tr");
        Object.values(dataRow).forEach((val) => {
            let cell = row.append("td");
            cell.text(val);

        });

    });

}
//Function to handle multiple filters
function updateFilters() {
    let state_name = d3.select("#state_name").property("value");
    let income = d3.select("#median_houshold_year_round_incomes").property("value");
    let family_size = d3.select("#Average_household_size").property("value");
    //let country = d3.select("#countryname").property("value");
    //let shape = d3.select("#shape").property("value"); 

    let filteredData = tableData;
    if (state_name) {
        // Apply `filter` to the table data to only keep the
        // rows where the `datetime` value matches the filter value
        filteredData = filteredData.filter(row => row.state_name === state_name);
    }
    //if (city) {
        // Apply `filter` to the table data to only keep the
        // rows where the `city` value matches the filter value
    //  //  filteredData = filteredData.filter(row => row.city === city);
   // }
    if (income) {
        // Apply `filter` to the table data to only keep the
        // rows where the `state` value matches the filter value
        filteredData = filteredData.filter(row => row.median_houshold_year_round_incomes >= income );
    }
    if (family_size) {
        // Apply `filter` to the table data to only keep the
        // rows where the `country` value matches the filter value
        filteredData = filteredData.filter(row => row.Average_household_size >= family_size);
    }
   // if (shape) {
        // Apply `filter` to the table data to only keep the
        // rows where the `shape` value matches the filter value
   //     filteredData = filteredData.filter(row => row.shape === shape);
    //}

    buildTable(filteredData);

}


d3.selectAll("#filter-btn").on("click", updateFilters);

// Build the table when the page loads
buildTable(tableData);
