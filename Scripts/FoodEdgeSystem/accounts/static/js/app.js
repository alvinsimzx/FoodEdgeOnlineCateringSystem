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

function validateMenuAdd(details)
{
    var itemName = document.getElementById("itemName").value; 
    var itemPrice = document.getElementById("itemPrice").value; 
    if(itemName == "" || itemPrice == "")
    {
        alert("Some fields are empty!"); 
    }
    else if(/^\d{1,3}$/.test(itemPrice) == false)
    {
        alert("Price should max 3 digits");
    }
    else
    {
        editBox(details); 
    }
}

function validateStock(details)
{
    var stockName = document.getElementById("stockName").value; 
    var amountLeft = document.getElementById("amountLeft").value;
    var deficit = document.getElementById("deficit").value;
    if(stockName == "" || amountLeft == "" || deficit == "")
    {
        alert("Some fields are empty!"); 
    }
    else if(/^\d{1,4}$/.test(amountLeft) == false)
    {
        alert("Current Amount should have max 4 digits");
    }
    else if(/^\d{1,5}$/.test(deficit) == false)
    {
        alert("Pricing should have max 5 digits");
    }
    else
    {
        editBox(details);
    }
}

function deleteBox(username) {
    var name = username.getAttribute("data-username");
    var box = document.getElementById('id01');
    box.style.display = "block";
    var deleteMessage = document.getElementById('deleteMessage');
    deleteMessage.innerHTML = "Confirm "+ name +" ?";
    var deleteConfirm = document.getElementById('deleteYes');
    deleteConfirm.innerHTML = "Delete";
    deleteConfirm.setAttribute("href", name);
}

function editBox(details){
    var name = details.getAttribute("data-username");
    var box = document.getElementById('id01');
    box.style.display = "block";
    var deleteMessage = document.getElementById('deleteMessage');
    deleteMessage.innerHTML = "Confirm "+ name +" ?";
    var deleteConfirm = document.getElementById('deleteYes');
    deleteConfirm.innerHTML = "Edit";
    deleteConfirm.removeAttribute("href");
    var id = details.getAttribute("data-form-id")
    deleteConfirm.setAttribute("onclick", "submitForm(\""+ id+"\")");
}


function submitForm(id) {
    document.getElementById(id).submit();
}

function openTab(evt, id) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(id).style.display = "block";
    evt.currentTarget.className += " active";
}

  function showComments(no){
    var commentsHide = document.getElementsByClassName("profile");
      for (i = 0; i < commentsHide.length; i++) {
        commentsHide[i].style.display = "none";
      }
    var comments = document.getElementById("set"+no);
    comments.style.display = "block";
    var commentScroll = document.getElementById("commentScroll"+no);
    commentScroll.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }