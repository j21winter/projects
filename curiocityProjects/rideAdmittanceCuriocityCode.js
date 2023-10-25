// curiosity code: 
// see createVariables Stretch 1/2 in codeChallenge_CreateVariables for improvement

//variables
var min_age = 10
var min_height = 42
var age; 
var height;
var num_height = numbers(height)
var height_approved;
var age_approved
var rider_qualifies;

// function to evaluate age
function ageEval(x){
    // block to decide if rider is old enough. Make variable age_approved and set to true or false
        if(x >= min_age){
            age_approved = true;
            console.log("Age approved: Yes ")
            return age_approved
            }
            else  
            {
            age_approved = false;
            console.log("Age approved: No")
            return age_approved
        }
    }
// function to evaluate age
function heightEval(y){ // block to decide if rider is old enough. Make variable age_approved and set to true or false
        if(y >= min_height){
            height_approved = true;
            console.log("Height approved: Yes")
            return age_approved
            }
            else  
            {
            height_approved = false;
            console.log("Height approved: No")
            return height_approved
            }
    }

    function riderApproval(x,y){ // Function to return rider approval based on true statements from age and height. 
        if( x == true && y == true){
            rider_qualifies = true
            console.log("Rider Approval: Approved")
        }
        else
        {
            rider_qualifies = false
            console.log("Rider Access: Denied")
        }
    }

ageEval(num_age)
heightEval(num_height)
riderApproval(age_approved,height_approved)
