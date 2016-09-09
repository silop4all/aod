

/////////////////////////////
// When the document is loaded:
/////////////////////////////
$(document).ready(function () {
    setTimeout(function () { l.hide() }, 1000);

    //////////////////////////////
    //   Personal information   //
    //////////////////////////////
    // Alter view
    $("#edit-personal-btn").click(function (event) {
        $(this).parent().addClass('hidden');
        $(".preview-personal-info").addClass('hidden');
        $("#personal-toolbar :nth-child(2)").removeClass('hidden');
        $(".editable-personal-info").removeClass('hidden');
    });
    // Cancel edit
    $("#reset-personal-btn").click(function () {
        $("#personal-toolbar :nth-child(1)").removeClass('hidden');
        $(".preview-personal-info").removeClass('hidden');
        $("#personal-toolbar :nth-child(2)").addClass('hidden');
        $(".editable-personal-info").addClass('hidden');
    });
    $("#save-personal-btn").click(function () {
        updatePersonalInfo();
    });


    //////////////////////////////
    //   Contact information    //
    //////////////////////////////
    // Alter view
    $("#edit-contact-btn").click(function () {
        $(this).parent().addClass('hidden');
        $(".preview-contact-info").addClass('hidden');
        $("#contact-toolbar :nth-child(2)").removeClass('hidden');
        $(".editable-contact-info").removeClass('hidden');
    });
    // Cancel edit
    $("#reset-contact-btn").click(function () {
        $("#contact-toolbar :nth-child(1)").parent().removeClass('hidden');
        $(".preview-contact-info").removeClass('hidden');
        $("#contact-toolbar :nth-child(2)").addClass('hidden');
        $(".editable-contact-info").addClass('hidden');
    });
    $("#save-contact-btn").click(function () {
        updateContactlInfo();
    });


    //////////////////////////////
    //   Platform information   //
    //////////////////////////////
    // Alter view
    $("#edit-platform-btn").click(function () {
        $(this).parent().addClass('hidden');
        $(".preview-platform-info").addClass('hidden');
        $("#platform-toolbar :nth-child(2)").removeClass('hidden');
        $(".editable-platform-info").removeClass('hidden');
    });
    // Cancel edit
    $("#reset-platform-btn").click(function () {
        $("#platform-toolbar :nth-child(1)").removeClass('hidden');
        $(".preview-platform-info").removeClass('hidden');
        $("#platform-toolbar :nth-child(2)").addClass('hidden');
        $(".editable-platform-info").addClass('hidden');
    });
    $("#save-platform-btn").click(function () {
        updatePlatformInfo();
    });


    // Manage the crowd-funding participation
    var crowdPartBtn = new Swap2Buttons($("#rg_crowd_funding_pos"), $("#rg_crowd_funding_neg"));
    $("#rg_crowd_funding_pos").click(function (event) {crowdPartBtn.click($(this));});
    $("#rg_crowd_funding_neg").click(function (event) {crowdPartBtn.click($(this));});

    // Manage the crowd-funding notification
    var crowdNotifyBtn = new Swap2Buttons($("#rg_crowd_funding_notify_pos"), $("#rg_crowd_funding_notify_neg"));
    $("#rg_crowd_funding_notify_pos").click(function (event) {crowdNotifyBtn.click($(this));});
    $("#rg_crowd_funding_notify_neg").click(function (event) {crowdNotifyBtn.click($(this));});

});

$("#edit-logo")
.mouseover(function () {
    $("#text").removeClass('hidden');
})
.mouseout(function () {
    $("#text").addClass('hidden');
});


//================================================
//==                    AJAX                    ==
//================================================

/////////////////////////////
// AJAX settings
/////////////////////////////
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});


/////////////////////////////
//  Check constraints
/////////////////////////////
function uniqueConstraint(endpoint, attribute) {
    var unique = true;
    $.ajax({
        type: 'GET',
        url: endpoint,
        headers: { 'Accept': 'application/json' },
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        data: { value: attribute.val()},
        async: false,
        success: function (state) {
            if (state.result > 0) {
                unique = false;
            }
        }
    });
    return unique;
}

///////////////////////////////
// Update the cover image (AJAX) - todo
///////////////////////////////
//function submitCoverImage() {
$("#cover-img").on(function (event) {
    //event.preventDefault();
    //loadCover($("#cover-img"));

    var form = $('#update-cover');
    var media = new FormData(form[0]);
    var link = form.find('input#cover-img').data('link');

    //var loading = new AjaxView(form);
    //loading.show();
    $.ajax({
        type: 'POST',
        url: link, //"/profile/media/1",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        cache: false,
        contentType: false,
        processData: false,
        data: media,
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
            //loading.hide();
            console.log("error 2");
        }
    });
    return false;
});


/////////////////////////////
// Update personal info (AJAX)
/////////////////////////////
function updatePersonalInfo() {
    var nameNode = $("#rg_name");
    var nameLabelNode = $("#rg_name_info");
    var lastnameNode = $("#rg_lastname");
    var lastnameLabelNode = $("#rg_lastname_info");
    var countryNode = $("#rg_country");
    var cityNode = $("#rg_city");
    var addressNode = $("#rg_address");
    var zipCodeNode = $("#rg_postal_code");
    // validate
    var nameState = validateName(nameNode, nameLabelNode);
    var surnameState = validateName(lastnameNode, lastnameLabelNode);
    var countryState = validateCountry(countryNode);
    if (!(nameState && surnameState && countryState)) { return false; }

    var data = {
        name: nameNode.val(), lastname: lastnameNode.val(), country: countryNode.val(),
        city: cityNode.val(), address: addressNode.val(), postal_code: zipCodeNode.val()
    };

    // submit data
    var loading = new AjaxView($('#account-info'));
    loading.show();
    $.ajax({
        type: 'POST',
        url: $("#save-personal-btn").data('url'),
        dataType: "html",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        data: JSON.stringify(data),
        cache: false,
        success: function (response) {
            $('#account-info').html(response);
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
            loading.hide();
        }
    });
}

/////////////////////////////
// Update contact info (AJAX)
/////////////////////////////
function updateContactlInfo() {
    var emailNode = $("#rg_email");
    var emailLabelNode = $("#rg_email_info");
    var mobileNode = $("#rg_mobile");
    // validate
    var emailState = validateEmail(emailNode, emailLabelNode);
    var mobileState = validateMobile(mobileNode);
    if (!(emailState && mobileState)) { return false; }
    
    var data = { email: emailNode.val(), mobile: mobileNode.val() };

    // submit data
    var loading = new AjaxView($('#contact-info'));
    loading.show();
    $.ajax({
        type: 'POST',
        url: $("#save-contact-btn").data('url'),
        dataType: "html",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        data: JSON.stringify(data),
        cache: false,
        success: function (response) {
            console.info("Contact information was updated!");
            $('#contact-info').html(response);
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
            loading.hide();
        }
    });
}

/////////////////////////////
// Update platform info (AJAX)
/////////////////////////////
function updatePlatformInfo() {
    var skillsNode = $("#rg_it_experience");    
    var rolesNode = $("#rg_role");
    var categoriesNode = $("#rg_channels");

    // validate
    var experienceState = validateExperience(skillsNode);
    var userRoleState = validateUserRole(rolesNode);
    var channelsState = validateChannels(categoriesNode);
    if (!(experienceState && userRoleState && channelsState)) { return false; }

    // Get the user's choices related to  crowd preferences 
    var data = { skills: skillsNode.val()[0], roles: rolesNode.val(), categories: categoriesNode.val() }
    var crowd = checkCrowdChoices();
    if (crowd["state"] === true) {
        data["crowd_participation"] = crowd["part"];
        data["crowd_notification"] = crowd["notify"];
    }

    // submit data
    var loading = new AjaxView($('#platform-info'));
    loading.show();
    $.ajax({
        type: 'POST',
        url: $("#save-platform-btn").data('url'),
        dataType: "html",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        data: JSON.stringify(data),
        cache: false,
        success: function (response) {
            console.info("Platform settings were updated!");
            $('#platform-info').html(response);
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
            loading.hide();
        }
    });
}


//================================================
//==                UI ACTIONS                  ==
//================================================

/////////////////////////////
//  Get crowd info
/////////////////////////////
function checkCrowdChoices() {
    var object = { "part": null, "notify": null, "state": false }
    if ($("#crowd-fund-participate").hasClass("hidden") === false) {
        object["part"] = ($("#crowd-fund-participate #rg_crowd_funding_pos").find("i").hasClass("fa-check-square-o") === true) ? 1 : 0;
        object["state"] = true;
    }
    if ($("#crowd-fund-notify").hasClass("hidden") === false) {
        object["notify"] = ($("#crowd-fund-notify #rg_crowd_funding_notify_pos").find("i").hasClass("fa-check-square-o") === true) ? 1 : 0;
        object["state"] = (object["state"] && true);
    }

    return object;
}

// Upload cover
function addCover() {
    $("#cover-img").click();
    return false;
}

function loadCover(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        }
        reader.readAsDataURL(input.files[0]);
    }

    var form = $('#update-cover');
    var media = new FormData(form[0]);
    var link = form.find('input#cover-img').data('link');

    $.ajax({
        type: 'POST',
        url: link,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        cache: false,
        contentType: false,
        processData: false,
        data: media,
        success: function (response) {
            if (response.state === "OK") {
                location.reload();
            }
            else {
                alert("The replace of the cover image fialed. Try again");
            }
        },
        error: function (response) {
            alert("The replace of the cover image fialed. Try again");
        }
    });
    return false;
}

// Upload logo
function addLogo() {
    $("#logo").click();
    return false;
}

function loadLogo(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        }
        reader.readAsDataURL(input.files[0]);
    }

    var form = $('#profileForm');
    var media = new FormData(form[0]);
    var link = form.find('input#logo').data('link');

    $.ajax({
        type: 'POST',
        url: link,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        cache: false,
        contentType: false,
        processData: false,
        data: media,
        success: function (response) {
            if (response.state === "OK") {
                location.reload();
            }
            else {
                alert("The replace of the logo failed. Try again");
            }
        },
        error: function (response) {
            alert("The replace of the logo failed. Try again");
        }
    });
    return false;
}


//================================================
//==                VALIDATION                  ==
//================================================

////////////////////////////
//      Name/Lastname
////////////////////////////
function validateName(name, label) {
    var regex = /^[^0-9!@#$%'^&_*]{2,50}$/;
    if (!regex.test(name.val())) {
        name.parent().addClass("has-error");
        label.removeClass("hidden");
        //label.tooltip('show');
        return false;
    }
    name.parent().removeClass("has-error");
    //label.tooltip('hide');
    label.addClass("hidden");
    return true;
}

$("#rg_name").keyup(function(){
    validateName($(this),$("#rg_name_info"));
});

$("#rg_lastname").keyup(function(){
    validateName($(this),$("#rg_lastname_info"));
});


////////////////////////////
//      Username 
////////////////////////////
function validateUsername(username, label) {
    label.empty();

    var regex = /^([a-zA-Z0-9]{4,})+([\!\@\#\$\%\&\_\-\.]{0,1})$/;
    var valid = true;
    var message = "";
    var unique = uniqueConstraint("username/", username);
        
    if (!regex.test(username.val())) {
        valid = false;
        message = "Type at least 4 characters<br>without spaces";
    }

    if (unique == false){
        message += (message.length > 0) ? " and select unique username" : "Type a non registered username";
    }

    if (!(valid && unique)) {
        username.parent().addClass("has-error");
        label.append(message);
        label.removeClass("hidden");
        return false;
    }

    username.parent().removeClass("has-error");
    label.addClass("hidden");
    return true;
}

$("#rg_username").keyup(function (event) {
    // check the validity of username after user's action
    validateUsername($(this), $("#rg_username_info"));
});


////////////////////////////
//      Password
////////////////////////////
function validatePwd(pass) {
    var regex = /^(?=^.{8,20}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/;
    var state = true;
    if (!regex.test(pass.val())) {
        state = false;
    }

    if (!state){
        pass.parent().addClass("has-error");
        $("#rg_pwd_info").removeClass("hidden");
        return false;
    }
    pass.parent().removeClass("has-error");
    $("#rg_pwd_info").addClass("hidden");
    return true;
}

$("#rg_pwd").keyup(function() {
    validatePwd($(this));
});


/////////////////////////
//   Confirm password
/////////////////////////
function confirmPwd(password, confirm) {
        
    if ( password.val() != confirm.val() ) {
        confirm.parent().addClass("has-error");
        $("#rg_pwd_confirm_info").removeClass("hidden");
        return false;
    }
    $("#rg_pwd_confirm_info").addClass("hidden");
    confirm.parent().removeClass("has-error");
    return true;
}

$('#rg_pwd_confirm').keyup(function() {
    confirmPwd($('#rg_pwd'), $(this));
});



////////////////////////////
//          Email
////////////////////////////
function validateEmail(email, label) {
    label.empty();

    var regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var valid = true;
    var message = "";
    var unique = uniqueConstraint($("#rg_email").data('url'), email);

    if (!regex.test(email.val())) {
        valid = false;
        message = "Invalid email";
    }

    if (unique == false){
        message += (message.length > 0) ? " - select <br/> a non registered email" : "Type a non registered email";
    }

    if (!(valid && unique)) {
        email.parent().addClass("has-error");
        label.append(message);
        label.removeClass("hidden");
        return false;
    }

    email.parent().removeClass("has-error");
    label.addClass("hidden");
    return true;
}
    
$("#rg_email").keyup(function (event) {
    //validateEmail($(this), $("#rg_email_info"));
});


////////////////////////////
//          Mobile
////////////////////////////
function validateMobile(mobile) {
    var regex = /^(?:[0-9]{10,15}|)$/;

    if (!regex.test(mobile.val())) {
        mobile.parent().addClass('has-error');
        $("#rg_mobile_info").removeClass('hidden');
        return false;
    }
    mobile.parent().removeClass('has-error');
    $("#rg_mobile_info").addClass('hidden');
    return true;
}

$("#rg_mobile").keyup(function(event) {
    validateMobile($(this));
});



////////////////////////////
//      Country
////////////////////////////
function validateCountry(country) {
    if (country.val() < 0 || country.val() === undefined || country.val() === null ){
        country.parent().addClass('has-error');
        $("#rg_country_info").removeClass("hidden");
        return false;
    }
    country.parent().removeClass('has-error');
    $("#rg_country_info").addClass("hidden");
    return true;
}

$("#rg_country").change(function(event){
    validateCountry($(this));
});



////////////////////////////
//      Experience
////////////////////////////
function validateExperience(experience){
    if (experience.val() < 0 || experience.val() === undefined || experience.val() === null) {
        experience.parent().addClass('has-error');
        $("#it-experience").addClass("error");
        $("#rg_it_experience_info").removeClass("hidden");
        return false;
    }
    experience.parent().removeClass('has-error');
    $("#it-experience").removeClass("error");
    $("#rg_it_experience_info").addClass("hidden");
    return true;
}

$("#rg_it_experience").change(function(event){
    validateExperience($("#rg_it_experience"));
});


///////////////////////
//   Roles
///////////////////////
function validateUserRole(roles){
    if ($("div.bootstrap-select").find("li.selected > a> span.text").length == 0 || roles.val() < 0 || roles.val() === undefined || roles.val() === null) {
        roles.parent().addClass('has-error');
        $("#user-role").addClass("error");
        $("#rg_role_info").removeClass("hidden");
        return false;
    }
    roles.parent().removeClass('has-error');
    $("#user-role").removeClass("error");
    $("#rg_role_info").addClass("hidden");
    return true;
}

$("#rg_role").change(function(event){
    validateUserRole($(this));
        
    if ($("#user-role > .bootstrap-select").find("li.selected > a> span.text").text().toLowerCase().indexOf("consumer") >= 0){
        $("#crowd-fund-participate").removeClass("hidden");
        $("#crowd-fund-notify").removeClass("hidden");
    }
    else {
        $("#crowd-fund-participate").addClass("hidden");
        $("#crowd-fund-notify").addClass("hidden");
    }
});


///////////////////////
//   Channels
///////////////////////
function validateChannels(channels){
    if ($("div.bootstrap-select").find("li.selected > a> span.text").length == 0 || channels.val() < 0 || channels.val() === undefined || channels.val() === null) {
        channels.parent().addClass('has-error');
        $("#channels").addClass('error');
        $("#rg_channels_info").removeClass("hidden");
        return false;
    }
    channels.parent().removeClass('has-error');
    $("#channels").removeClass('error');
    $("#rg_channels_info").addClass("hidden");
    return true;
}

$("#rg_channels").change(function(event){
    validateChannels($(this));
});


