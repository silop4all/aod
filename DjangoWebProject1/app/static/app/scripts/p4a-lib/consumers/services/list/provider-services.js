$(function () {
    $('#table').bootstrapTable({
        data: data
    });

    $('#table').parent().css("height", "auto");

    $("#new-service").click(function (event) {
        window.location.href += "/services";
    });

});

function editFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar edit-service" href="javascript:void(0)" title="Edit the service">',
        '<i class="fa fa-pencil-square-o fa-lg text-success"></i>',
        '</a>'
    ].join('');
}

function removeFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar delete-service" href="javascript:void(0)" title="Remove the service">',
        '<i class="fa fa-trash-o fa-lg text-danger"></i>',
        '</a>'
    ].join('');
}

function statsFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar stats-service" href="javascript:void(0)" title="Show statistics">',
        '<i class="fa fa-bar-chart fa-lg text-primary"></i>',
        '</a>'
    ].join('');
}

window.statsActionEvent = {
    'click .stats-service': function (e, value, row, index) {
        window.location.href = row.url + "#stats";
    }
};

window.editActionEvent = {
    'click .edit-service': function (e, value, row, index) {
        window.location.href = row.url +"modify";
    }
};


window.removeActionEvent = {
    'click .delete-service': function (e, value, row, index) {
        deleteService(row.url);
    }
};

