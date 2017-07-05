var service = -1;

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

$(document).ready(function () {
    service = $("#title").data().serviceId;
    var url = window.location.pathname;

    $("#delete_service").click(function (e) {
        e.preventDefault();
        deleteService($(this));
    });
    $("#edit_service").click(function () {
        editService(url);
    });

    $(".various").fancybox({
        maxWidth: 1000,
        maxHeight: 600,
        fitToView: false,
        width: '100%',
        height: '75%',
        autoSize: false,
        closeClick: false,
        openEffect: 'none',
        closeEffect: 'none'
    });

    
    $.ajax({
        type: 'GET',
        url: $("#info").data('resource'),
        headers: { "Accept": "application/json", "Content-Type": "application/json", },
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            //
            // load map if constraint
            //
            if (response.location_constraint === true) {
                GoogleMap.load({ 'latitude': response.latitude, "longitude": response.longitude, "radius": response.coverage }, response.title);
            }
        },
        error: function (response) {
            console.error(gettext("load service details error"));
        },
        complete: function () {
            // nth
        }
    });

    $("#download_sw").click(function (event) {
        event.preventDefault();
        window.location.href = $(this).data().link;
    });



}).on('click', '#stats_tab', function () {
    // load from server

}).on('click', '#support_tab', function () {
    //
    // Load technical support for service
    //
    // var loading = new AjaxView($("#support_container"));
    // loading.show();
    var skype = "";
    var materialsList = "";

    $.ajax({
        type: 'GET',
        url: $(this).data('resource'),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            skype = response.skype;
            if (response.technical_support.length) {

                for (i in response.technical_support) {
                    //
                    // Clarify cases considering the type of the technical material
                    //
                    switch (response.technical_support[i].technical_support.alias) {
                        case "shared_link":
                            var icon = { "level1": { "color": " text-primary" }, "level2": { "icon": " fa-link" } };
                            var hrefAction = '<a target="_blank" class="btn btn-danger pull-right" href="' + response.technical_support[i].link + '">' + gettext('Open') + ' <span class="fa fa-external-link"></span></a>';
                            materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            break;

                        case "youtube_video":
                            var icon = { "level1": { "color": " text-danger" }, "level2": { "icon": " fa-youtube-play" } };
                            var hrefAction = '<a class="various fancybox.iframe btn btn-danger pull-right"  href="' + response.technical_support[i].link + '">' + gettext('Attend') + ' <span class="fa fa-play-circle-o"></span></a>';
                            materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            break;

                        case "vimeo_video":
                            var icon = { "level1": { "color": " text-info" }, "level2": { "icon": " fa-vimeo" } };
                            var hrefAction = '<a class="various fancybox.iframe btn btn-danger pull-right"  href="' + response.technical_support[i].link + '">' + gettext('Attend') + ' <span class="fa fa-play-circle-o"></span></a>';
                            materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            break;

                        case "video":
                            if ($.inArray(response.technical_support[i].extension, ["mp4", "mp3"]) > -1) {
                                var icon = { "level1": { "color": "text-info" }, "level2": { "icon": " fa-video-camera" } };
                                var hrefAction = '<a class="various btn btn-danger pull-right" data-fancybox-type="iframe" href="' + response.technical_support[i].path + '">' + gettext('Open') + ' <span class="fa fa-play-circle-o"></span></a>';
                                materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            }
                            break;

                        case "document":
                            if ($.inArray(response.technical_support[i].extension, ["doc", "docx"]) > -1) {
                                var icon = { "level1": { "color": " text-primary" }, "level2": { "icon": " fa-file-word-o" } };
                                var hrefAction = '<a class="various btn btn-danger pull-right" href="' + response.technical_support[i].path + '">' + gettext('Download') + ' <span class="fa fa-download"></span></a>';
                                materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            }
                            else if ($.inArray(response.technical_support[i].extension, ["xls", "xlsx"]) > -1) {
                                var icon = { "level1": { "color": " text-success" }, "level2": { "icon": " fa-file-excel-o" } };
                                var hrefAction = '<a class="various btn btn-danger pull-right" href="' + response.technical_support[i].path + '">' + gettext('Download') + ' <span class="fa fa-download"></span></a>';
                                materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            }
                            else if ($.inArray(response.technical_support[i].extension, ["ppt", "pptx"]) > -1) {
                                var icon = { "level1": { "color": " text-danger" }, "level2": { "icon": " fa-file-powerpoint-o" } };
                                var hrefAction = '<a class="various btn btn-danger pull-right" href="' + response.technical_support[i].path + '">' + gettext('Download') + ' <span class="fa fa-download"></span></a>';
                                materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            }
                            else if ($.inArray(response.technical_support[i].extension, ["pdf"]) > -1) {
                                var icon = { "level1": { "color": " text-danger" }, "level2": { "icon": " fa-file-pdf-o" } };
                                var hrefAction = '<a class="various btn btn-danger pull-right" data-fancybox-type="iframe" href="' + response.technical_support[i].path + '">' + gettext('Open') + ' <span class="fa fa-arrows-alt"></span></a>';
                                materialsList += formatListItem(response.technical_support[i], icon, hrefAction);
                            }
                            //else if ($.inArray(response.technical_support[i].extension, ["png", "gif", "jpeg", "jpg"]) > -1) {
                            //}
                            break;
                        default:
                            console.log(response.technical_support[i].extension + " extension is not supported");
                            break;
                    }
                }
            }
            // Append list items
            $("#materials-list").html(materialsList);
            // Append Skype details
            var skypeID = 'Not available';
            if (skype != '' && skype != null) {
                $("#service-provider-skype-parent").removeClass('hidden');
                skypeID = [
                    '<div style="clear: both" class="padding-left-20">',
                        '<span>' + gettext("ID") + ': </span>',
                        skype,
                    '<div>',

                    '<div id="SkypeButton_Call_' + skype + '_1">',
                        '<script type="text/javascript">',
                        'Skype.ui({"name": "chat", "element": "SkypeButton_Call_' + skype + '_1", "participants": ["' + skype + '"], "imageSize": 24});',
                    '</script>',
                   '</div>'
                ].join('');
            }
            else {
                skypeID = "<div class='alert alert-danger'><strong style='font-size: large'>" + gettext("Skype account not available") + "</strong></div>"
            }
            $("#service-provider-skype").html(skypeID);
        },
        error: function (response) {
            console.error('error');
        },
        complete: function () {
            // loading.hide();
        }
    });

}).on('click', '.access-resource', function () {

    var targetVideo = $(this).attr('href');
    $(targetVideo).toggle('fast');

}).on('click', '#reviews_tab', function () {

    // Updates the stars layout
    var score = parseFloat($("#review_score").text());
    if (score !== "None" && !(isNaN(score))) {
        for (var j = 1; j <= Math.ceil(score) ; j++) {
            if (j > score){
                $("#stars-area").find(".star-rating-" + j).removeClass("fa-star-o").addClass("fa-star-half-full");
            }
            else{
                $("#stars-area").find(".star-rating-" + j).removeClass("fa-star-o").addClass("fa-star");
            }
        }
    }   

}).on('mouseover', ".list-group-item", function () {
    $(this).addClass('active');
}).on('mouseleave', ".list-group-item", function () {
    $(this).removeClass('active');
});



function loadReviewBars(total, counters) {
    for (var i in counters) {
        
        var progress = Math.ceil(counters[i] * 100 / total);
        var selector = "#" + i + "_star";
        $(selector).css('width', progress + '%').attr('aria-valuenow', progress);

        var bgSelector = selector + "_bg";
        $(bgSelector).html(counters[i]).css('background', 'green');
    }
}

function loadImageSlider() {
    var options = {
        $AutoPlay: true,
        $ArrowNavigatorOptions: {
            $Class: $JssorArrowNavigator$,
            $ChanceToShow: 2,
        },
        $SlideshowOptions: {
            $Class: $JssorSlideshowRunner$,
            $Transitions: [{ $Duration: 700, $Opacity: 2, $Brother: { $Duration: 100, $Opacity: 2 } }],
            $TransitionsOrder: 1,
            $ShowLink: true
        },
        /*
        $ThumbnailNavigatorOptions: {
            $Class: $JssorThumbnailNavigator$,
            $ChanceToShow: 2
        }
        */
    };
    var jssor_slider1 = new $JssorSlider$('slider', options);
}

function deleteService(service) {
    var loading = new AjaxView($(".platform-info-box"));
    var auth = "";
    
    loading.show();
    $.ajax({
        type: 'DELETE',
        url: service.attr('href'),
        async: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            auth = response.auth_basic;
            console.log(gettext("Success service deletion"));
        },
        error: function (response) {
            console.error(gettext('The deletion of this service failed'));
        },
        complete: function () {
            //
            // Remove service from Social network
            // 
            if (service.data('social-network-usage') === "True") {
                $.ajax({
                    type: 'GET',
                    url: service.data('social-network-delete-url'),
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
            location.href = service.data('redirect');
            loading.hide();
        }
    });
    return true;
}


function formatListItem(material, icon, action) {
    //
    // Prepare the technical material layout in order to be appended in list
    //
    return [
        '<li class="list-group-item">',
            '<span class="fa-stack fa-2x margin-right-5">',
                '<span class="fa fa-circle fa-stack-2x ' + icon.level1.color + '"></span>',
                '<span class="fa ' + icon.level2.icon + ' fa-stack-1x fa-inverse"></span>',
            '</span>',
            '<strong>' + material["title"] + '</strong>',
            action,
            (material.description !== null) ? '<div>' + material.description + '</div>' : "",
            (material.software_dependencies !== null) ? '<div>' + material.software_dependencies + '</div>' : "",
        '</li>',
    ].join('');
}


