$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

var purchaseTableSelector = '#purchased-services-table';


$(document).on('click', '.nas-select-btn', function () {
    var payload = {
        service_id: $(this).data('serviceId'),
        consumer_id: $(this).data('consumerId')
    };
    var url = $(this).data('url');
    popTemporalService(url, payload);
}).on('all.bs.table', purchaseTableSelector, function (name, args) {
    $("td").each(function () {
        $(this).css('vertical-align', 'middle').attr('role', 'navigation');
    });
}).on('page-change.bs.table', purchaseTableSelector, function (name, args) {
    $("#purchased-services-table").bootstrapTable('check', 0);
}).on('check.bs.table ', purchaseTableSelector, function (name, service) {

    $.ajax({
        type: 'GET',
        url: service.details_url,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            $(".bought-service-view").removeClass('hidden');

            // set image
            var imageElement = '';
            if (response.image != null && response.image.includes("/")) {
                var img = response.image.split("/");
                imageElement = '<img src="' + service.image_url + img[img.length - 1] + '" alt="' + gettext("Service logo") + '" class="img-responsive img-rounded" style="max-height:200px; border-radius:3px 3px" />';
            }
            else {
                imageElement = [
                    '<div class="col-sm-12 col-xs-12 text-center" style="background-color: lightgray; opacity: 0.5; font-size: 20pt; padding: 30px; border-radius: 2px">',
                        '<span class="fa fa-photo fa-5x" style="color:rgba(0,0,0,0.15)"></span>',
                    '</div>'
                ].join('');
            }
            $("#bought-service-img").html(imageElement);

            $("#bought-service-title").text(response.title);
            $("#bought-service-title").parent().attr("title", gettext("The service title is ") + response.title);
            $("#bought-service-descr").text(response.description);

            var categories = '';
            for (var j in response.categories) {
                categories += "<span class='label label-md label-info'>" + response.categories[j].title + "</span>,";
            }
            $("#bought-service-categories").html(categories.slice(0, -1));

            if (response.price > 0) {
                $("#bought-service-price").html(response.unit + " " + Math.round(response.price, 2));
            }
            else {
                $("#bought-service-price").html("-");
            }
            $("#bought-service-policy").text(response.charging_policy.name);

            if (response.type == "H") {
                $(".bought-machine-service").addClass('hidden');
                $("#bought-service-type").html("<span class='fa fa-users fa-lg'></span>" + gettext("Human-based"));
                $("#bought-service-installation").text(response.installation_guide);
            }
            else {
                $(".bought-machine-service").removeClass('hidden');
                $("#bought-service-type").html("<span class='fa fa-laptop fa-lg'></span>" + gettext("Machine-based"));
                $("#bought-service-license").html(response.license + " (version: " + response.version + ")");
                $("#bought-service-installation").text(response.installation_guide);
            }

            var languages = "All languages are supported";
            if (response.languages.length) {
                languages = '';
                for (i in response.languages) {
                    languages += "<span class='label label-info'>" + response.languages[i].alias + "</span> ";
                }
            }
            $("#bought-service-languages").html(languages);

            if (response.location_constraint) {
                $("#bought-service-map").removeClass('hidden');
                var coordinates = { "latitude": response.latitude, "longitude": response.longitude, "radius": response.coverage, "serviceTitle": response.title };
                getMap(coordinates, 'map');
            }
            else {
                $("#bought-service-map").addClass('hidden');
            }

            $("#bought-service-other-constraints").text(response.constraints);

            $("#bought-service-requirements").text(response.requirements);
            $("#bought-service-usage-guide").text(response.usage_guidelines);

            // Display link if any
            if (response.link != null && response.link !== "") {
                var linkElem = '<a href="' + response.link + '" title="'+ gettext("Useful link") +'">' + response.link + '</a>';
                $("#bought-service-link").html(linkElem);
                $("#bought-service-link").parent().removeClass('hidden');
            }
            else {
                $("#bought-service-link").parent().addClass('hidden');
            }

            // Load configuration (default or updated)
            var config = '';
            if (response.configuration.length > 0) {
                $.ajax({
                    type: 'GET',
                    url: service.config_url,
                    beforeSend: function (xhr, settings) {
                        $.ajaxSettings.beforeSend(xhr, settings);
                    },
                    contentType: 'application/json',
                    success: function (response) {
                        var configData = response.results[0].configuration;
                        config += "<ul>";
                        for (var i in configData) {
                            config += [
                                '<li>',
                                    '<strong>' + configData[i].parameter + ': </strong>',
                                    configData[i].value,
                                '</li>',
                            ].join('');
                        }
                        config += "</ul>";
                        $("#bought-service-configuration").parent().removeClass('hidden');
                        $("#bought-service-configuration").html(config);
                    }
                });
            }
            else {
                $("#bought-service-configuration").parent().addClass('hidden');
                $("#bought-service-configuration").html(config);
            }
            

            var videos = gettext('Service owner does not provide videos'), docs = gettext('Service owner does not provide further documents (pdf, office documents, images, etc..)');
            if (response.technical_support.length) {
                videos = '';
                docs = '';
                for (i in response.technical_support) {
                    if ($.inArray(response.technical_support[i].format, ["mp4", "mp3"]) > -1) {
                        videos += [
                            '<div data-support-id="' + response.technical_support[i].id + '">',
                                '<span class="fa fa-video-camera text-muted fa-lg" role="img" alt="' + gettext("Video presentation") + '"></span> ',
                                '<a href="#vd' + response.technical_support[i].id + '" class="access-resource text-primary">' + response.technical_support[i].title + '</a><br>',
                                '<video style="display:none; width:100%" controls  title="' + response.technical_support[i].title + '" id="vd' + response.technical_support[i].id + '">',
                                    '<source src="' + response.technical_support[i].path + '" type="video/mp4">',
                                    '<source src="movie.ogg" type="video/ogg">',
                                    gettext('Your browser does not support the video tag.'),
                                '</video>',
                            '</div>'
                            ].join('');
                    }
                    else if ($.inArray(response.technical_support[i].format, ["doc", "docx"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "'>";
                        docs += "<span class='fa fa-file-word-o text-primary fa-lg' role='img' alt='" + gettext("Office word document") + "'></span> <a href='#wd" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='wd" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["xls", "xlsx"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "'>";
                        docs += "<span class='fa fa-file-excel-o text-success fa-lg' role='img' alt='" + gettext("Office Excel dociument") + "'></span> <a href='#wd" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='wd" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["pdf"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "'>";
                        docs += "<span class='fa fa-file-pdf-o text-danger fa-lg' role='img' alt='" + gettext("Pdf document") + "'></span> <a href='#pdf" + response.technical_support[i].id + "' class='access-resource text-primary'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none; width: 100%; min-height:100%' title='" + response.technical_support[i].title + "' width='540' id='pdf" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                    else if ($.inArray(response.technical_support[i].format, ["png", "gif", "jpeg", "jpg"]) > -1) {
                        docs += "<div data-support-id='" + response.technical_support[i].id + "'>";
                        docs += "<span class='fa fa-file-picture-o text-primary fa-lg' role='img' alt='" + gettext("Image file") + "'></span> <a href='#img" + response.technical_support[i].id + "' class='access-resource'>" + response.technical_support[i].title + "</a><br>";
                        docs += "<iframe style='display:none' title='" + response.technical_support[i].title + "' width='540' id='img" + response.technical_support[i].id + "' height='360' frameborder='0' src='" + response.technical_support[i].path + "' ebkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>";
                        docs += "</div>";
                    }
                }
            }
            $("#bought-service-support-videos").html(videos);
            $("#bought-service-support-docs").html(docs);

            // skype
            var skypeID = 'Not available';
            if (response.skype != '' && response.skype != null) {
                skypeID = [
                    '<div id="SkypeButton_Call_' + response.skype + '_1">',
                        '<script type="text/javascript">',
                        'Skype.ui({"name": "chat", "element": "SkypeButton_Call_' + response.skype + '_1", "participants": ["' + response.skype + '"], "imageSize": 24});',
                    '</script>',
                   '</div>'
                ].join('');
            }
            $("#bought-service-provider-skype").empty().append(skypeID);

        },
        error: function (response) {
            swal({
                html: false,
                title: gettext("Network of assistance services"),
                text: gettext('Sorry, an error has occurred'),
                type: "warning",
                confirmButtonText: gettext("Try again!"),
                confirmButtonColor: "#d9534f"
            });
        },
        complete: function () {
            $(".bought-service-view").fadeIn();
        }
    });

}).on('click', '.access-resource', function () {
    var targetVideo = $(this).attr('href');
    $(targetVideo).toggle('fast');

}).on('click', '.swap-tab', function () {
        //var url = location.href.split("#");
        //location.href = url[0] + $(this).attr('href');
}).on('mouseover', "h3", function () {

    $(this).css('text-decoration', 'underline');

}).on('mouseleave', "h3", function () {
    $(this).css('text-decoration', 'none');

}).on('mouseover', ".info-block", function () {
    $(this).css('background', 'rgba(230, 230, 230, 0.58)');

}).on('mouseleave', ".info-block", function () {
    $(this).css('background', 'whitesmoke');
});

var getMap = function getMap(obj, elemID) {
    // Initiate variables
    var lat, lng;
    // Initiate coordinates
    var coordinates = new google.maps.LatLng(obj.latitude, obj.longitude);
    // Set options
    var mapOptions = {
        zoom: 12,
        center: coordinates,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        panControl: false,
        scaleControl: false,
        streetViewControl: false,
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL,  //enables the dimension
            position: google.maps.ControlPosition.RIGHT_BOTTOM  //position enables
        },
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        }
    };

    var map = new google.maps.Map(document.getElementById(elemID), mapOptions);
    var marker = new google.maps.Marker({
        position: coordinates,
        map: map,
        draggable: false
    });

    var coverage = new google.maps.Circle({
        strokeColor: 'red',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#AAAAAA',
        fillOpacity: 0.4,
        map: map,
        center: coordinates,
        radius: obj.radius * 1000
    });


    var infoWindow = new google.maps.InfoWindow({
        content: "<div><strong>" + gettext("Service") + ":</strong> " + obj.serviceTitle + " <br><strong>" + gettext("Latitude") + ":</strong> " + obj.latitude + "<br><strong>" + gettext("Longitude") + ":</strong> " + obj.longitude + "</div>"
    });

    // Handle user actions
    google.maps.event.addListener(marker, 'click', function (event) {
        infoWindow.open(map, marker);
    });
    // Set marker in center
    map.setCenter(marker.position);
    marker.setMap(map);
}



function setTypeFormatter(value, row, index) {
    if (value == "H") {
        return '<span class="fa fa-users fa-lg"></span>' + gettext('Human-based');
    }
    return '<span class="fa fa-laptop fa-lg"></span>' + gettext('Machine-based');
}

function setRemoveFormatter(value, row, index) {
    return [
        '<button class="btn btn-danger btn-xs nas-select-btn" data-url="' + row['url'] + '" data-service-id="' + row["id"] + '" data-index="'+index+'" data-consumer-id="' + row["consumerId"] + '">',
            '<span class="fa fa-remove fa-lg  cursor-pointer"></span> <span>' + gettext('Remove') + '</span>',
        '</button>',
    ].join('');
}

function popTemporalService(url, payload) {
    $.ajax({
        type: 'DELETE',
        url: url,
        data: JSON.stringify(payload),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            swal({
                html: false,
                title: gettext("Remove an insteresting service"),
                text: gettext('Sorry, an error has occurred'),
                type: "warning",
                confirmButtonText: gettext("Try again!"),
                confirmButtonColor: "#d9534f"
            });
        },
        complete: function () {}
    });
    return true;
}
