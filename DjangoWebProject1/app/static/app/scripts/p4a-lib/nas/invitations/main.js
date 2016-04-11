// JS file

var emailRegex = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

$(document).ready(function () {
    $('#invite-carers-table').bootstrapTable({ data: [] });
    $(".fixed-table-body").css("height", "auto");

    var kwdElem = $("#carer_email_account");
    var searchBtnElem = $("#retrieve-users");
    var errorMessage = $("#error-message");
    var timer = 0;

    $("#carer_email_account").keyup(function () {
        var element = $(this);

        // clear any interval on key up
        clearInterval(timer);

        // check the validity of username after user's action
        timer = setTimeout(
            function () {
                if (kwdElem.val() == "" || !emailRegex.test(kwdElem.val())) {
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
            600
        );
    });

    $("#retrieve-carers").click(function () {
        if (validateInput(kwdElem, searchBtnElem, errorMessage) != 1) {
            return;
        }
        $('#invite-carers-table').bootstrapTable('destroy');

        // search if consumer with the incoming email account exists
        var loading = new AjaxView($('#invite-carers-table'));
        loading.show();

        $.ajax({
            type: 'GET',
            url: "/api/v1/assistance/carers",
            data: { email: $("#carer_email_account").val() },
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            headers: { "accept": "application/json" },
            contentType: 'application/json',
            success: function (response) {
                $('#invite-carers-table').bootstrapTable({ data: response.results });
                $(".fixed-table-body").css("height", "auto");
            },
            error: function (response) {
                console.log("GET: /api/v1/assistance/carers?email=xxx");
            },
            complete: function () {
                loading.hide();
            }
        });
    });

}).on("click", ".invite-btn", function () {
    $(document).css('cursor', 'progress');
    submitPermissionRequest($(this));
    $(this).addClass('disabled');
    $(document).css('cursor', 'default');
});


function sendInvitationFormatter(value, row, index) {
    return [
        '<button class="btn btn-link invite-btn" data-user-id="' + row['id'] + '" data-name="' + row['name'] + '" data-lastname="' + row['lastname'] + '" title="Express your interest">',
            '<span class="fa fa-envelope-o fa-lg text-success"></span>',
        '</button>'
    ].join('');
}

function validateInput(kwdElem, searchBtnElem, errorMessage) {
    // validate the email input   

    if (kwdElem.val() == "" || !emailRegex.test(kwdElem.val())) {
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

function submitPermissionRequest(user) {
    var receiver = user.data('name') + " " + user.data('lastname');
    var loading = new AjaxView($('#search-results-table'));

    $.ajax({
        type: 'POST',
        url: "/assistance/invitations",
        data: JSON.stringify({ target: user.data('userId') }),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            var content = "Your invitation has been sent on " + receiver + ".";
            if (response.message !== undefined) {
                content = response.message;
            }
            swal({
                title: "Network of carers",
                text: content,
                type: "success",
                confirmButtonText: "Continue",
                confirmButtonColor: "#228B22"
            });
        },
        error: function (response) {
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
