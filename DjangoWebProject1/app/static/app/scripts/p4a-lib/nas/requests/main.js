$(document).ready(function () {
    $('#carer-requests-table').bootstrapTable({
        data: carerRequests
    });

    $('#consumer-requests-table').bootstrapTable({
        data: consumerRequests
    });
    
    $(".fixed-table-body").css("height", "auto");


    $("#new-service").click(function (event) {
        window.location.href += "/services";
    });


    $(".delete-interest").click(function () {
        deleteNasRequest($(this));
    });


    $(document).on('click', '#cancel-assist-request', function () {
        swal({
            html: false,
            title: "Cancel assistance request",
            text: "In case you cancel your assistance to a person with disabilities, the selected and purchased services will not be removed.",
            type: "info",
            confirmButtonText: "Continue!",
            confirmButtonColor: "#3a87ad",
            confirmButtonClass: "btn-info",
            showCancelButton: false
        });
    });

    setTable();

    // auto refresh page
    setTimeout(autoRefresh, 1000 * 300);
});

$("body").on('all.bs.table', '#carer-requests-table', function (name, args) {
    setTable();
});
$("body").on('all.bs.table', '#consumer-requests-table', function (name, args) {
    setTable();
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

function autoRefresh() {
    location.reload();
}

function setTable() {
    $("span").tooltip({ trigger: "hover" });
    $("a").tooltip({ trigger: "hover" });
    $("label").tooltip({ trigger: "hover" });
    $("td").each(function () {
        $(this).css("vertical-align", "middle");
    });
}

function editFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar edit-service" href="javascript:void(0)" title="Edit the service">',
            '<span class="fa fa-pencil-square-o fa-lg text-success"></span>',
        '</a>'
    ].join('');
}

function removeInterestFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar delete-interest" href="javascript:void(0)" data-placement="bottom" title="Cancel your assistance on ' + row['user_info'] + ' without the network removal" data-request-id="' + row['id'] + '">',
            '<span class="fa fa-remove fa-lg text-danger"></span> <span class="text-danger">Cancel</span>',
        '</a>'
    ].join('');
}

function setNetworkFormatter(value, row, index) {
    if (row['request_state'] == "True") {
        return [
            '<a class="btn btn-link" href="/assistance/configuration/' + row['consumer_id'] + '" data-placement="bottom" title="Set up the network of assistance services of ' + row['user_info'] + '" data-request-id="' + row['consumer_id'] + '">',
                '<span class="fa fa-play-circle fa-lg text-success"></span> <span class="text-success">Start</span>',
            '</a>'
        ].join('');
    }
    return [
    '-'
    ].join('');
}

function previewNetworkFormatter(value, row, index) {
    if (row['request_state'] == "True") {
        return [
            '<a class="btn btn-link" data-consumer-id="' + row['consumer_id'] + '" href="/assistance/services/preview/' + row['consumer_id'] + '" data-placement="bottom" title="Access the network of assistance services of ' + row['user_info'] + '">',
            '<i class="fa fa-search fa-lg text-info"></i> <span class="text-primary">View</span>',
            '</a>'
        ].join('');
    }
    return [
    '-'
    ].join('');
}

function setRequestResponseFormatter(value, row, index) {
    if (row['request_response'] == "False") {
        return '<label class="label label-warning" data-placement="bottom" title="The response in this request is still pending">NO</label>';
    }
    else{
        return '<label class="label label-success" data-placement="bottom" title="The response in this request is still pending">YES</label>';
    }
}

function setRequestStateFormatter(value, row, index) {
    if (row['request_response'] == "True") {
        if (row['request_state'] == "True") {
            return '<label class="label label-success" data-placement="bottom" title="Your assistance request has accepted">Accepted</label>';
        }
        return '<label class="label label-danger" data-placement="bottom" title="Your assistance request has rejected">Forbidden</label>';
    }
    return '<label class="label label-warning" data-placement="bottom" title="Your assistance request is still pending">Pending</label>';
}

function deleteNasRequest(element) {
    var endpoint = "/assistance/requests/" + element.data('request-id');

    $.ajax({
        type: 'DELETE',
        url: endpoint,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {}
    });
    return true;
}

