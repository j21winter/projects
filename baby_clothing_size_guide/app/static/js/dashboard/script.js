// Main Dashboard functions

// VARIABLES
// results card filters
let display_child = document.getElementById("display_child").value
console.log(display_child);

let resultFilter = document.getElementById("result_filter").value
console.log(resultFilter);

// DEFAULT CALL TO SHOW ALL
console.log("filterSelection(all,all) GETTING ALL RESULTS")
filterSelection()

// MAIN FILTER FUNCTION
function filterSelection(){
    let display_child = document.getElementById("display_child").value
    console.log(display_child);

    let resultFilter = document.getElementById("result_filter").value
    console.log(resultFilter);
    
    var allCards = document.getElementsByClassName("result_card")

    // Iterate through every single one and check for compliance
    for(var i = 0; i < allCards.length; i++){
        // if it contains the child and result filter add show to its class
        // if it doesn't contain child and result filter remove show from its class.
        allCards[i].classList.contains(display_child) && allCards[i].classList.contains(resultFilter) ? showElement(allCards[i]) : hideElement(allCards[i])
    }
}

// SHOW ELEMENT FUNCTION
function showElement(element){
    console.log("showing element");
    element.classList.remove("hide")
}

// HIDE ELEMENT FUNCTION
function hideElement(element){
    console.log("hiding element");
    element.classList.add("hide")
}



