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

    $("#delete_service").click(function () {
        deleteService(url);
    });
    $("#edit_service").click(function () {
        editService(url);
    });

    // Preview tab: slider
    loadImageSlider();
    
    $.ajax({
        type: 'GET',
        url: "/api/v1/services/" + service,
        headers: { "Accept": "application/json", "Content-Type": "application/json", },
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            // load map
            GoogleMap.load({ 'latitude': response.latitude, "longitude": response.longitude, "radius": response.coverage }, response.title);
        },
        error: function (response) {
            console.error("load service details error")
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
    var loading = new AjaxView($("#stats_container"));
    loading.show();
    var url = "/api/v1/services/" + service + "/reviews";

    $.ajax({
        type: 'GET',
        url: url,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            console.log("Get stats");
            $("#stats_table").bootstrapTable({ data: [] });
        },
        error: function (response) {
            console.error('error');
        },
        complete: function () {
            loading.hide();
        }
    });

    $('.fixed-table-body').css('height', 'auto');

}).on('click', '#support_tab', function () {
    var loading = new AjaxView($("#support_container"));
    loading.show();
    var url = "/api/v1/services/" + service + "/support";

    var videos = 'Service owner does not provide videos';
    var docs = 'Service owner does not provide further documents (pdf, office documents, images, etc..)';
    var skype = "magnitakis";
    $.ajax({
        type: 'GET',
        url: url,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            console.log(response);
            skype = response.skype;
            if (response.technical_support.length) {
                videos = '';
                docs = '';
                for (i in response.technical_support) {
                    if ($.inArray(response.technical_support[i].format, ["mp4", "mp3"]) > -1) {
                        videos += [
                            '<div data-support-id="' + response.technical_support[i].id + '">',
                                '<span class="fa fa-video-camera text-muted fa-lg" role="img" alt="Video presentation"></span> ',
                                '<a href="#vd' + response.technical_support[i].id + '" class="access-resource text-primary">' + response.technical_support[i].title + '</a><br>',
                                '<video style="display:none; width:80%" controls  title="' + response.technical_support[i].title + '" id="vd' + response.technical_support[i].id + '">',
                                    '<source src="' + response.technical_support[i].path + '" type="video/mp4">',
                                    '<source src="movie.ogg" type="video/ogg">',
                                    'Your browser does not support the video tag.',
                                '</video>',
                            '</div>'
                        ].join('');
                    }
                    else if ($.inArray(response.technical_support[i].format, ["doc", "docx"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "' style=' min-height: 80px; min-width: 45%; background: #E6E6E6; padding: 30px; float: left; margin: 10px' >";
                        docs += "<span style='vertical-align: middle;' class='fa fa-file-word-o text-primary fa-2x' role='img' alt='Office word document'></span> <a href='#wd" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='wd" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["xls", "xlsx"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "' style=' min-height: 80px; min-width: 45%; background: #E6E6E6; padding: 30px; float: left; margin: 10px' >";
                        docs += "<span style='vertical-align: middle;' class='fa fa-file-excel-o text-success fa-2x' role='img' alt='Office Excel dociument'></span> <a href='#wd" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='wd" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["pdf"]) > -1) {
                        docs += "<span data-support-id='" + response.technical_support[i].id + "' style=' min-height: 80px; min-width: 45%; background: #E6E6E6; padding: 30px; float: left; margin: 10px'>";
                        docs += "<span style='vertical-align: middle;' class='fa fa-file-pdf-o text-danger fa-2x' role='img' alt='Pdf document'></span> <a href='#pdf" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none; width: 100%; min-height:100%' title='" + response.technical_support[i].title + "' width='540' id='pdf" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</span>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["png", "gif", "jpeg", "jpg"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "'  style=' min-height: 80px; min-width: 45%; background: #E6E6E6; padding: 30px; float: left; margin: 10px'>";
                        docs += "<span style='vertical-align: middle;' class='fa fa-file-picture-o text-primary fa-2x' role='img' alt='Image file'></span> <a href='#img" + response.technical_support[i].id + "' class='access-resource'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='img" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                }
            }
            $("#service-support-videos").html(videos);
            $("#service-support-docs").html(docs);

            var skypeID = 'Not available';
            if (skype != '' && skype != null) {
                skypeID = [
                    '<div style="clear: both" class="padding-left-20">',
                        '<span>ID: </span>',
                        skype,
                    '<div>',

                    '<div id="SkypeButton_Call_' + skype + '_1">',
                        '<script type="text/javascript">',
                        'Skype.ui({"name": "chat", "element": "SkypeButton_Call_' + skype + '_1", "participants": ["' + skype + '"], "imageSize": 22});',
                    '</script>',
                   '</div>'
                ].join('');
            }
            $("#service-provider-skype").empty().append(skypeID);
        },
        error: function (response) {
            console.error('error');
        },
        complete: function () {
            loading.hide();
        }
    });

}).on('click', '.access-resource', function () {
    var targetVideo = $(this).attr('href');
    $(targetVideo).toggle('fast');
}).on('click', '#reviews_tab', function () {
    var loading = new AjaxView($("#reviews_container"));
    loading.show();
    var url = "/api/v1/services/" + service + "/reviews";

    $.ajax({
        type: 'GET',
        url: url,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (response) {
            var reviewsNum = response.results.length;
            var reviewsSum = 0;
            var counters = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
            var text = [
                    '<div class="jumbotron text-center">',
                        'No user feedback.',
                    '</div>'
            ].join('');

            $("#reviews_number").text(reviewsNum);
            if (reviewsNum) {
                text = '';
                for (var i in response.results) {
                    if (response.results[i].rating != null && response.results[i].rating != "") {
                        console.log(i - reviewsNum - 1);
                        text += [
                            '<div style="clear:both; ' + ((i != reviewsNum - 1) ? 'border-bottom:1px solid rgba(190, 190, 190, 0.70)' : '') + '" class="row margin-bottom-10">',
                                '<div class="col-sm-4 col-lg-4 col-md-4 col-xs-12" >',
                                    '<center>',
                                        '<span class="fa-stack fa-3x">',
                                            '<span class="fa fa-circle fa-stack-2x" style="color: #d7d5d5 "></span>',
                                            '<span class="fa fa-user fa-stack-1x" style="color: #ebebea"></span>',
                                        '</span>',
                                        '<h6 ><span> By <a href="#" title="User feedback for the service">' + response.results[i].consumer.user.lastname + " " + response.results[i].consumer.user.name + '</a></span></h6>',
                                        '<h6 ><span class="fa fa-calendar text-primary"></span> ' + response.results[i].purchased_date.split('T')[0] + '</h6>',
                                    '</center>',
                                '</div>',
                                '<div class="col-sm-8 col-lg-8 col-md-8 col-xs-12" >',
                                    '<div style="clear:both">',
                                        '<span class="fa fa-star-o fa-lg  star-colorize-yellow star-rating-1"></span>',
                                        '<span class="fa fa-star-o fa-lg  star-colorize-yellow star-rating-2"></span>',
                                        '<span class="fa fa-star-o fa-lg  star-colorize-yellow star-rating-3"></span>',
                                        '<span class="fa fa-star-o fa-lg  star-colorize-yellow star-rating-4"></span>',
                                        '<span class="fa fa-star-o fa-lg  star-colorize-yellow star-rating-5"></span>',
                                        '<span>  ' + response.results[i].rating + ' / 5</span>',
                                    '</div>',
                                    '<div class="text-justify">',
                                        '<span>' + response.results[i].rating_rationale + '</span>',
                                    '</div>',
                                '</div>',
                            '</div>'
                        ].join('');
                        reviewsSum += response.results[i].rating;
                        counters[response.results[i].rating]++;
                    }
                }
                $("#reviews_column").html(text);
            }
            else{
                $(".reviews_container").html(text);
            }
            //$("#reviews_average").html(Math.round(reviewsSum / reviewsNum), 2);
            $("#reviews_average").html((reviewsSum / reviewsNum));
            loadReviewBars(reviewsNum, counters);
        },
        error: function (response) {
            console.error('error');
        },
        complete: function () {
            loading.hide();
        }
    });
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
                //window.location.href = response.redirect;
                location.href = "/offerings";
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