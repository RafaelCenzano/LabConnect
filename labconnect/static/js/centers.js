function submitForm(center_name) {
    var form = document.getElementById("center_form");
    form.action+=center_name;
    var submitbtn = document.getElementById("submitButton");
    submitbtn.submit();
}


function assignFunctionToCenters() {
    var center_input = document.getElementById("center_name")
    
    var centers = document.getElementsByClassName("center");
    for (var i = 0; i < centers.length; i++) {
        centers[i].addEventListener("click", function () {
            center_input.value = centers[i].id;
            submitForm(centers[i].id);
        });
    }
}