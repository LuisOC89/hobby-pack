function showPeople() {
    //Get checkbox
    var toShowCheckBox = document.getElementById("specificPeople");
    //Get element I want to change
    var shadowp = document.getElementsById("hiddenPeople");    
    //If checkbox is checked, I want to show the people hiding in that <div>
    if (toShowCheckBox.checked == true){
        shadowp.style.display = "block";
    } else if (toShowCheckBox.checked == false){
        shadowp.style.display = "none";
    }
}

function myFunction() {
    var checkBox = document.getElementById("myCheck");
    var text = document.getElementById("text");
    var shadowp2 = document.getElementsById("test2");
    if (checkBox.checked == true){
        text.style.display = "block";
        shadowp2.style.display = "block";
    } else {
       text.style.display = "none";
       shadowp2.style.display = "none";
    }
}

/*$(function(){
    $('#specific_people').click(function(){ 
          var showHide =$(this).is(':checked');// returns boolean
          $('.to-hide').toggle( showHide );

    });
});*/



