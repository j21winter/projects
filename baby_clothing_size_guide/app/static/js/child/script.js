// Child dashboard functions

// VARIABLES
// results card filters
let resultFilter = document.getElementById("result_filter")

// DEFAULT CALL TO SHOW ALL
console.log("filterSelection(all) GETTING ALL RESULTS")
filterSelection("all")

// MAIN FILTER FUNCTION
function filterSelection(filterString){

    var allCards = document.getElementsByClassName("result_card")

    // Iterate through every single one and check for compliance
    for(var i = 0; i < allCards.length; i++){
        // if it contains the filterString add show to its class
        // if it doesn't contain filterString remove show from its class.
        allCards[i].classList.contains(filterString) ? showElement(allCards[i]) : hideElement(allCards[i])
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



