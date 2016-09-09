var emailRegex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;


$(document).ready(function () {
    // initiate
    $('#search-results-table').bootstrapTable({
        data: []
    });
    $(".fixed-table-body").css("height", "auto");


    var kwdElem = $("#consumer_email_account");
    var searchBtnElem = $("#retrieve-users");
    var errorMessage = $("#error-message");
    var timer = 0;
    

    $("#consumer_email_account").keyup(function () {
        var element = $(this);

        // clear any interval on key up
        clearInterval(timer);

        // check the validity of username after user's action
        timer = setTimeout(
            function () {
                if (kwdElem.val() == "" || !emailRegex.test(kwdElem.val()) ) {
                    kwdElem.parent().addClass('has-error');
                    searchBtnElem.addClass('disabled');
                    errorMessage.removeClass('hidden');
                }
                else {
                    kwdElem.parent().removeClass('has-error');
                    searchBtnElem.removeClass('disabled');
                    errorMessage.addClass('hidden');
                }
            },
            300
        );
    });


    $("#retrieve-users").click(function () {
        if (validateInput(kwdElem, searchBtnElem, errorMessage) != 1) {
            return;
        }

        // empty the contents of the bootstrap table
        $('#search-results-table').bootstrapTable('destroy');

        // get user input
        var keywords = $("#consumer_email_account").val();

        // search if consumer with the incoming email account exists
        retrieveRegisteredUsers(keywords);
    });

});


function validateInput(kwdElem, searchBtnElem, errorMessage) {
    // validate the email input   

    if (kwdElem.val() == "" || !emailRegex.test(kwdElem.val()) ) {
        kwdElem.parent().addClass('has-error');
        searchBtnElem.addClass('disabled');
        errorMessage.removeClass('hidden');
        return -1;
    }
    else {
        kwdElem.parent().removeClass('has-error');
        searchBtnElem.removeClass('disabled');
        errorMessage.addClass('hidden');
        return 1;
    }
}


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});


function retrieveRegisteredUsers(email) {

    var loading = new AjaxView($('#search-results'));
    loading.show();
    $.ajax({
        type: 'GET',
        url: $("#retrieve-users").data('filter'),
        data: {email: email},
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
            $('#search-results-table').bootstrapTable({
                data: response.users
            });
            $(".fixed-table-body").css("height", "auto");
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
            loading.hide();
        }
    });
    return true;
}


$(document).on("click", ".declare-interest-btn", function () {
    $(document).css('cursor', 'progress');
    submitPermissionRequest($(this));
    $(this).addClass('disabled');
    $(document).css('cursor', 'default');
})


function submitPermissionRequest(user) {
    var receiver = user.data('name') + " " + user.data('lastname');
    var loading = new AjaxView($('#search-results-table'));

    $.ajax({
        type: 'POST',
        url: $(".declare-interest-btn").data('resource'),
        data: JSON.stringify({ consumer_id: user.data('userId') }),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            swal({
                title: "Network of assistance services ",
                text: "You need permission from " + receiver + " to setup his/her network of assistance services on behalf of him/her.\nYour request has been submitted.",
                type: "success",
                confirmButtonText: "Continue",
                confirmButtonColor: "#228B22"
            });

        },
        error: function (response) {
            console.log("error");
            swal({
                title: "Network of assistance services ",
                text: "An error occurred an your request has been abandoned.",
                type: "warning",
                confirmButtonText: "Sorry, try again!",
                confirmButtonColor: "#b94a48"
            });
        },
        complete: function () {
            loading.hide();
        }
    });
    return true;
}
