


// Fetch the JSON data and console log it
d3.json("/brands").then(function(myData) {
    console.log(myData);
    makeMenus(myData);
    // load all data
    buildTable(myData);

});


// Use D3 to select the table body
var tbody = d3.select("tbody");

// ------------------------------------------------
// populate the drop-down menues

function makeMenus(myData){
    const menus = ["brand", "ranking_category", "product_category"];

    menus.forEach(menu => {
            var options = myData.map(item => item[menu]);
            options = [...new Set(options)].sort();
            console.log(options);
            populateDrop(menu, options);
})
}


function populateDrop(drop, dropVals) {
    var dropElement = d3.select("#" + drop);
    dropVals.forEach((dropVal) => {
        var option = dropElement.append("option");
        option.text(dropVal);
        option.attr("value", dropVal);
        }
    );
};


// ------------------------------------------------

//Function to populate table with all or user filtered data
// Build table by loop myData and get keys/vals write cells
function buildTable(brands){
    tbody.html("");//remove any rows of data from the table
    brands.forEach((brand) => {
        // Append one table row per object
        var row = tbody.append("tr");
        // append one td for each key value
        Object.entries(brand).forEach(([key, value]) => {
        var cell = row.append("td");
        //set the td value to the key value
        cell.text(value);
        });
    });
};

// // ------------------------------------------------
// //Build a table filter for user to select options
var button = d3.select("#filter-btn");
var form = d3.select("form");

// //handlers
button.on("click", filterData);
form.on("submit", filterData);

//function to filter data
function filterData() {
    //interupt page refresh if user press enter/return
    d3.event.preventDefault();

    // Select the input element and get the raw HTML node
    let brandElement = d3.select("#brand");
    let rankElement = d3.select("#ranking_category");
    let prodElement = d3.select("#product_category");

 
    // Get the value property of the datetimeElement / input element
    let searchParams = {}
    
    let brand = brandElement.property("value");
    let rankingCat = rankElement.property("value");
    let prodCat = prodElement.property("value");

    let url = "/brands/" + brand + "/" + rankingCat + "/" + prodCat;

    d3.json(url).then(function(filterData) {
        console.log(filterData);
        // load data
        buildTable(filterData);
    
    });
    
    
    // call function to build the table with filtered data
    buildTable(filterData);
};