$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

// Delete a service instance
function deleteService(service) {
    var loading = new AjaxView($(".platform-info-box"));
    loading.show();
    var successUrl = "";
    var auth = ""; 

    $.ajax({
        type: 'DELETE',
        url: service.url,
        async: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            successUrl = response.redirect;
            auth = response.auth_basic;
        },
        error: function (response) {
            alert(gettext('The deletion of this service failed in AOD'));
        },
        complete: function () {
            //
            // Remove service from Social network
            // 
            if (service.social_network_usage === "True") {
                $.ajax({
                    type: 'GET',
                    url: service.social_network_delete_url,
                    headers: {
                        "Authorization": "Basic " + auth
                    },
                    success: function (response) {
                    },
                    error: function (response) {
                        console.error(gettext('The deletion of this service failed in SN'));
                    },
                    complete: function () {
                        loading.hide();
                    }
                });
            }
            window.location.href = successUrl;
            loading.hide();
        }
    });
    return true;
}