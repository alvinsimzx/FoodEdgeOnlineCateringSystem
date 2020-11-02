window.addEventListener('scroll', function(){
    const parallax = document.querySelector('.bigBanner');
    const opacity = document.querySelector('.opacity');
    let scroll = window.pageYOffset;

    parallax.style.transform = 'translateY('+ scroll*.3+'px)';
    opacity.style.opacity =  scroll / (sectionY.top + section_height);
})

$(function(){
    $("#fname_error_message").hide();
    $("#lname_error_message").hide();
    $("#email_error_message").hide();

    var error_fname = false;
    var error_lname = false;
    var error_email = false;

    $("#fname").focusout(function(){
        check_name("#fname_error_message", "#fname");
    });
    $("#lname").focusout(function(){
        check_name("#lname_error_message", "#lname");
    });
    $("#email").focusout(function(){
        check_email();
    });
    
    function check_name(error_message, name){
        var pattern = /^[a-zA-Z]*$/;
        var fname = $(name).val();
        if (pattern.test(fname) && fname !== '') {
            $(error_message).hide();
            $(name).css("border","2px solid lime");
        }else{
            $(error_message).html("Only Characters are allowed");
            $(error_message).css("color", "red");
            $(error_message).show();
            $(name).css("border","2px solid red");
            if (name === "#fname"){
                error_fname = true;
            }else if (name === "#lname"){
                error_lname = true;
            }
            
        }
    }
    
    function check_email(){
        var pattern = /^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$/;
        var email = $("#email").val();
        if (pattern.test(email) && email !== ''){
            $("#email_error_message").hide();
            $("#email").css("border","2px solid lime");
        }else{
            $("#email_error_message").html("Invalid email address");
            $("#email_error_message").css("color", "red");
            $("#email_error_message").show();
            $("#email").css("border","2px solid red");
            error_email = true;
        }
    }

    $("#feedback").submit(function(){
        var error_fname = false;
        var error_lname = false;
        var error_email = false;

        check_name("#fname_error_message", "#fname");
        check_name("#lname_error_message", "#lname");
        check_email();

        if (error_fname === false && error_lname === false && error_email === false){
            alert ("Submitted successfully!");
            return true;
        }else {
            alert ("Invalid form input please try again");
            return false;
        }
    });

});



function deleteBox(username) {
    var name = username.getAttribute("data-username");
    var box = document.getElementById('id01');
    box.style.display = "block";
    var deleteMessage = document.getElementById('deleteMessage');
    deleteMessage.innerHTML = "Delete "+ name +"'s account?";
    var deleteConfirm = document.getElementById('deleteYes');
    deleteConfirm.setAttribute("href", "/delete/"+name);
}

function editBox(){
    var box = document.getElementById('id02');
    box.style.display = "block";
}