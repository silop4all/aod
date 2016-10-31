$(function () {
    $('#table').bootstrapTable({
        data: data
    });

    $('#table').parent().css("height", "auto");

    $("#new-service").click(function (event) {
        location.href = $(this).data('href');
    });

});

function editFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar edit-service" href="javascript:void(0)" title="' + gettext("Edit the service") + '">',
            '<span class="fa fa-pencil-square-o fa-lg text-success"></span>',
        '</a>'
    ].join('');
}

function removeFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar delete-service" href="javascript:void(0)" title="' + gettext("Remove the service") + '">',
            '<span class="fa fa-trash-o fa-lg text-danger"></span>',
        '</a>'
    ].join('');
}

function statsFormatter(value, row, index) {
    return [
        '<a class="btn btn-toolbar stats-service" href="javascript:void(0)" title="' + gettext("Show statistics") + '">',
            '<span class="fa fa-bar-chart fa-lg text-primary"></span>',
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
        deleteService(row);
    }
};

