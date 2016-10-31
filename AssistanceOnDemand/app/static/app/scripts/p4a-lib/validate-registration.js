// Global timers
var usernameTimer = 0, emailTimer = 0, pwdConfirmTimer = 0;


/////////////////////////////
//  Swap crowd buttons view
/////////////////////////////
$(document).ready(function () {

    // Manage the crowd-funding participation
    var crowdPartBtn = new Swap2Buttons($("#rg_crowd_funding_pos"), $("#rg_crowd_funding_neg"));
    $("#rg_crowd_funding_pos").click(function (event) { crowdPartBtn.click($(this)); });
    $("#rg_crowd_funding_neg").click(function (event) { crowdPartBtn.click($(this)); });

    // Manage the crowd-funding notification
    var crowdNotifyBtn = new Swap2Buttons($("#rg_crowd_funding_notify_pos"), $("#rg_crowd_funding_notify_neg"));
    $("#rg_crowd_funding_notify_pos").click(function (event) { crowdNotifyBtn.click($(this)); });
    $("#rg_crowd_funding_notify_neg").click(function (event) { crowdNotifyBtn.click($(this)); });

});


///////////////////////////
//  Form Validation
///////////////////////////
$("form").submit(function (event) {
    // initiate status
    var state = true;

    // Swap the embedded icon of submit button
    $("#registry-submit").find("span").addClass("fa-spin fa-spinner");

    // Fields validation
    var nameState = validateName($("#rg_name"), $("#rg_name_info"));
    var surnameState = validateName($("#rg_lastname"), $("#rg_lastname_info"));
    var usrState = validateUsername($("#rg_username"), $("#rg_username_info"));
    var pwdState = validatePwd($("#rg_pwd"));
    var confirmState = confirmPwd($("#rg_pwd"), $("#rg_pwd_confirm"));
    var emailState = validateEmail($("#rg_email"), $("#rg_email_info"));
    var mobileState = validateMobile($("#rg_mobile"));
    var countryState = validateCountry($("#rg_country"));
    var experienceState = validateExperience($("#rg_it_experience"));
    var userRoleState = validateUserRole($("#rg_role"));
    // alter it
    //var channels = validateChannels($("#rg_channels"));
    var answer = validateQuestion($("#rg_question"));

    // Get the user's choices related to  crowd preferences 
    var crowd = checkCrowdChoices();
   
    // Swap the embedded icon of submit button (again)
    $("#registry-submit").find("span").addClass("fa-check").removeClass("fa-spin fa-spinner");

    //return (nameState && surnameState && usrState && pwdState && confirmState && emailState && countryState && experienceState && userRoleState && answer);
    if (!(nameState && surnameState && usrState && pwdState && confirmState && emailState && countryState && experienceState && userRoleState && answer)) {
        return false;
    }

    // Create a JS object
    var data = {
        rg_name: $("#rg_name").val(), rg_lastname: $("#rg_lastname").val(), rg_username: $("#rg_username").val(),
        rg_pwd: $("#rg_pwd").val(), rg_email: $("#rg_email").val(), rg_mobile: $("#rg_mobile").val(), rg_country: $("#rg_country").val()[0],
        rg_it_experience: $("#rg_it_experience").val()[0], rg_role: $("#rg_role").val(), rg_channels: [1],/*$("#rg_channels").val()*/

    };
    if (crowd["state"] === true) {
        data["crowd_participation"] = crowd["part"];
        data["crowd_notification"] = crowd["notify"];
    }

    // Upload data
    var loading = new AjaxView($("#registrationForm"));
    loading.show();
    $.ajax({
        type: 'POST',
        url: "validation/",
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify(data),
        //async: false,
        async: true,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            console.log(response);
            if (response.state === true) {
                window.location = response.redirect;
            }
            else {
                alert(gettext("Oops, an error is occured!!!"));
            }
        },
        error: function(response){
            alert(gettext("Oops, an error is occured!!!"));
        },
        complete: function () {
            loading.hide();
        }
    });

    return false;
});

////////////////////////////
//  Unused functions
////////////////////////////
function serializeChannels() {
    var selectedValues = [];
    $("#rg_channels :selected").each(function () {
        selectedValues.push($("#rg_channels").val());
    });
    return selectedValues;
}

function serializeRoles() {
    var selectedValues = [];
    $("#rg_role :selected").each(function () {
        selectedValues.push($("#rg_role").val());
    });
    return selectedValues;
}


////////////////////////////
//      Name/Last name
////////////////////////////
function validateName(name, label) {
    var regex = /^[^0-9!@#$%'^&_*]{2,50}$/;
    if (!regex.test(name.val())) {
        name.parent().addClass("has-error");
        label.removeClass("hidden");
        return false;
    }
    name.parent().removeClass("has-error");
    label.addClass("hidden");
    return true;
}

$("#rg_name").keyup(function () {
    validateName($(this), $("#rg_name_info"));
});

$("#rg_lastname").keyup(function () {
    validateName($(this), $("#rg_lastname_info"));
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
        message = gettext("Type at least 4 characters<br>without spaces");
    }

    if (unique == false) {
        message += (message.length > 0) ? gettext(" and select unique username") : gettext("Type a non registered username");
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
    var element = $(this);
    // clear any interval on key up
    clearInterval(usernameTimer);  
    // check the validity of username after user's action
    usernameTimer = setTimeout(
        function () {
            validateUsername(element, $("#rg_username_info"));
        },
        600
    );
});


////////////////////////////
//      Password
////////////////////////////
function validatePwd(pass) {
    var regex = /^(?=^.{8,20}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[a-z]).*$/;
    var state = true;
    if (!regex.test(pass.val())) {
        state = false;
    }

    if (!state) {
        pass.parent().addClass("has-error");
        $("#rg_pwd_info").removeClass("hidden");
        return false;
    }
    pass.parent().removeClass("has-error");
    $("#rg_pwd_info").addClass("hidden");
    return true;
}

$("#rg_pwd").keyup(function () {
    validatePwd($(this));
});

// Show the strength level of password
function progressBar(color, curValue) {
    return '<div class="progress-bar ' + color + '" role="progressbar" id="my_bar" aria-valuenow="' + curValue + '" aria-valuemin="0" aria-valuemax="100" style="width: ' + curValue + '%">' +
            '<span class="sr-only">' + curValue + gettext('% Complete (success)') + '</span>' +
        '</div>';
}



/////////////////////////
//   Confirm password
/////////////////////////
function confirmPwd(password, confirm) {

    if (password.val() != confirm.val() || confirm.val().length < 1) {
        confirm.parent().addClass("has-error");
        $("#rg_pwd_confirm_info").removeClass("hidden");
        return false;
    }
    $("#rg_pwd_confirm_info").addClass("hidden");
    confirm.parent().removeClass("has-error");
    return true;
}

$('#rg_pwd_confirm').keyup(function () {
    var element = $(this);
    // clear any interval on key up
    clearInterval(pwdConfirmTimer);
    // check the validity of username after user's action
    pwdConfirmTimer = setTimeout(
        function () {
            confirmPwd($('#rg_pwd'), element);
        },
        400
    );
});



////////////////////////////
//          Email
////////////////////////////
function validateEmail(email, label) {
    label.empty();

    var regex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var valid = true;
    var message = "";
    var unique = uniqueConstraint("email/", email);

    if (!regex.test(email.val())) {
        valid = false;
        message = gettext("Invalid email");
    }

    if (unique == false) {
        message += (message.length > 0) ? gettext(" - select <br/> a non registered email") : gettext("Type a non registered email");
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
    var element = $(this);

    // clear any interval on key up
    clearInterval(emailTimer);  
    // check if user's email exists - unique constraint
    emailTimer = setTimeout(
        function () {
            validateEmail(element, $("#rg_email_info"));
        },
        800
    );
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

$("#rg_mobile").keyup(function (event) {
    validateMobile($(this));
});



////////////////////////////
//      Country
////////////////////////////
function validateCountry(country) {
    if (country.val() < 0 || country.val() === undefined || country.val() === null) {
        country.parent().addClass('has-error');
        $("#country").addClass("error");
        $("#rg_country_info").removeClass("hidden");
        return false;
    }
    country.parent().removeClass('has-error');
    $("#country").removeClass("error");
    $("#rg_country_info").addClass("hidden");
    return true;
}

$("#rg_country").change(function (event) {
    validateCountry($(this));
});



////////////////////////////
//      Experience
////////////////////////////
function validateExperience(experience) {
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

$("#rg_it_experience").change(function (event) {
    validateExperience($("#rg_it_experience"));
});


///////////////////////
//   Roles
///////////////////////
function validateUserRole(roles) {
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

$("#rg_role").change(function (event) {
    validateUserRole($(this));

    if ($("#user-role > .bootstrap-select").find("li.selected > a> span.text").text().toLowerCase().indexOf("consumer") >= 0) {
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
function validateChannels(channels) {
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

$("#rg_channels").change(function (event) {
    validateChannels($(this));
});


///////////////////////
//   Questions
///////////////////////
function validateQuestion(answer) {
    var d = $("span#literal").text().split("+");
    var sum = parseInt(d[0]) + parseInt(d[1]);
    if (answer.val() != sum ) {
        answer.parent().addClass("has-error");
        $("#rg_question_info").removeClass("hidden");
        return false;
    }
    answer.parent().removeClass("has-error");
    $("#rg_question_info").addClass("hidden");
    return true;
}

$("#rg_question").keyup(function (event) {
    validateQuestion($(this));
});



/////////////////////////////
//  Get method - AJAX
/////////////////////////////
function uniqueConstraint(endpoint, attribute) {
    var unique = true;
    $.ajax({
        type: 'GET',
        url: endpoint,
        headers: { 'Accept': 'application/json' },
        data: { value: attribute.val()},
        "beforeSend": function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        async: false,
        success: function (state) {
            if (state.result > 0) {
                unique = false;
            }
        }
    });
    return unique;
}


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



$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});
