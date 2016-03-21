$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

// Delete a service instance
function deleteService(url) {
    var loading = new AjaxView($(".platform-info-box"));
    loading.show();
    $.ajax({
        type: 'DELETE',
        url: url,
        async: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            if (response.state === true) {
                window.location.href = response.redirect;
            }
        },
        error: function (response) {
            alert('The deletion of this service failed');
        },
        complete: function () {
            loading.hide();
        }
    });
    return true;
}