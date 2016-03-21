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
            confirmButtonText: "Ok, continue!",
            confirmButtonColor: "#3a87ad",
            confirmButtonClass: "btn-info",
            showCancelButton: false
        });
    })

});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

function editFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar edit-service" href="javascript:void(0)" title="Edit the service">',
        '<i class="fa fa-pencil-square-o fa-lg text-success"></i>',
        '</a>'
    ].join('');
}

function removeInterestFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar delete-interest" href="javascript:void(0)" title="Remove your interest" data-request-id="' + row['id'] + '">',
        '<i class="fa fa-remove fa-lg text-danger"></i>',
        '</a>'
    ].join('');
}

function setNetworkFormatter(value, row, index) {
    if (row['request_state'] == "True") {
        return [
            '<a class="btn btn-link" href="/network-assistance-services/configuration/' + row['consumer_id'] + '" title="Set up the network of assistance services" data-request-id="' + row['consumer_id'] + '">',
            '<i class="fa fa-play-circle fa-lg text-success"></i>',
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
            '<a class="btn btn-link" data-consumer-id="' + row['consumer_id'] + '" href="/network-assistance-services/services/preview/'+row['consumer_id']+'" title="Preview the network of assistance services">',
            '<i class="fa fa-search fa-lg text-info"></i>',
            '</a>'
        ].join('');
    }
    return [
    '-'
    ].join('');
}

function setRequestResponseFormatter(value, row, index) {
    console.log(row);

    if (row['request_response'] == "False") {
        return '<label class="label label-warning" title="The response in this request is still pending">NO</label>';
    }
    else{
        return '<label class="label label-success" title="The response in this request is still pending">YES</label>';
    }
}

function setRequestStateFormatter(value, row, index) {
    if (row['request_response'] == "True") {
        if (row['request_state'] == "True") {
            return '<label class="label label-success" title="The response in this request is still pending">Accepted</label>';
        }
        return '<label class="label label-danger" title="The response in this request is still pending">Forbidden</label>';
    }
    return '<label class="label label-warning" title="The response in this request is still pending">Pending</label>';
}

function deleteNasRequest(element) {
    var loading = new AjaxView($('#carer-requests-table'));
    var endpoint = "/network-assistance-services/requests/" + element.data('request-id');

    loading.show();
    $.ajax({
        type: 'delete',
        url: endpoint,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            console.log(response);
            console.info(response.data);
            //$('#carer-requests-table').bootstrapTable('destroy');
            //$('#carer-requests-table').bootstrapTable({
            //    data: response.data
            //});
            //$(".fixed-table-body").css("height", "auto");
            location.reload();
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

function previewNetwork(targetUser) {
    $.ajax({
        type: 'post',
        url: "/network-assistance-services/services/preview",
        data: JSON.stringify({ "consumer_id": targetUser }),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
        },
        error: function (response) {
            console.log("error");
        },
        complete: function () {
        }
    });
    return true;
}



