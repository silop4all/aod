// On document ready..
$(document).ready(function () {
    // load categories in as a tree
    $.ajax({
        type: 'GET',
        url: "/api/v1/categories/tree",
        data: { level: 0 },
        headers: { "accept": "application/json", "content-type": "application/json" },
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            // @todo on update
            var categoriesLists = [];
    
            var options = '';
            var data = response.results;
            for (var root in data) {
                options += '<optgroup label="' + data[root].title + '">';

                var childs = data[root].children;
                for (var i in childs) {
                    if ($.inArray(childs[i].id, categoriesLists) > -1) {
                        options += '<option value="' + childs[i].id + '" title="' + childs[i].title + '" selected>' + childs[i].title + ' </option>';
                    }
                    else {
                        options += '<option value="' + childs[i].id + '" title="' + childs[i].title + '">' + childs[i].title + ' </option>';
                    }
                    

                    var leafs = childs[i].children;
                    for (var j in leafs) {
                        if ($.inArray(leafs[j].id, categoriesLists) > -1) {
                            options += '<option data-content="<span class=\'padding-left-20\'>  ' + leafs[j].title + '</span>" data-icon="fa fa-minus" value="' + leafs[j].id + '" selected>' + leafs[j].title + '</option>';
                        }
                        else {
                            options += '<option data-content="<span class=\'padding-left-20\'>  ' + leafs[j].title + '</span>" data-icon="fa fa-minus" value="' + leafs[j].id + '">' + leafs[j].title + '</option>';
                        }
                    }
                }
                options += '</optgroup>';
            }
            $("#srv_category").append(options);
            $("#srv_category").selectpicker('refresh');
        },
        error: function (response) {
            console.error(response);
        },
        complete: function () {
        }
    });


    $("div#service-registration-wizard > div > ul > li").click(function () {
        return preventClickTab($(this));
    });

    // Initiate tooltip
    //$("[data-toggle=tooltip]").tooltip();
    //$('input').tooltip({ trigger: "hover" });

    ///////////////////////////
    // 1st step: Basic
    ///////////////////////////
    
    // Logo
    $("#srv_logo").change(function () {
        loadLogo(this);
    });

    $("#srv_cover_image").change(function () {
        var list = $("#srv_cover_image :selected").attr('value').split('/');
        $("#srv_cover_image :selected").text(list[list.length - 1]);
    });

    $(".cover-name").each(function () {
        var list = $(this).text().split('/');
        $(this).text(list[list.length - 1]);
    });

    $("div.cover-selection").click(function (event) {
        event.preventDefault();
        var choice = $(this).data().image;
        $('#srv_cover_image').selectpicker('val', choice);
        $("#srv_cover_image").find('option[value="' + choice + '"]').attr('selected', true);
    })

    // Keywords
    $("#add_new_srv_keyword").click(function (event) {
        appendServiceKeyword();
        //return false;
    });

    $('#srv_keyword').keypress(function (e) {
        var key = e.which;
        if (key == 13)  {
            appendServiceKeyword();
        }
    });
    $("#remove_srv_keyword").click(function () {
        removeServiceKeywords();
    });


    ///////////////////////////
    // 2nd step: Usage
    ///////////////////////////
    $("#srv_charging_model").change(function () {
        if ($("#srv_charging_model :selected").attr('value') == "1") {
            $("#srv_price").val('0.00').attr('readonly', true);
            $("#srv_price").parent().removeClass("has-error");
            $("#srv_currency").attr('readonly', true);
        }
        else{
            $("#srv_price").val('').removeAttr('readonly', false);
            $("#srv_currency").removeAttr('readonly', false);
        }
    });

    ///////////////////////////
    // 3rd step: Usage
    ///////////////////////////

    // Software package
    $("#srv_software").change(function () {
        loadPackage(this);
    });

    // Define the target users of the new service
    var crowdPartBtn = new Swap2Buttons($("#srv_availability_pb"), $("#srv_availability_pr"));
    $("#srv_availability_pb").click(function (event) { crowdPartBtn.click($(this)); $("#set_target_users").addClass('hidden'); });
    $("#srv_availability_pr").click(function (event) { crowdPartBtn.click($(this)); $("#set_target_users").removeClass('hidden'); });

    // Send to wish list
    $("#send_to_wish_list").click(function () {
        sendItemsWishList();   
    })

    // Return to email list
    $("#send_to_email_list").click(function () {
        removeItemsWishList();
    })


    ///////////////////////////
    // 4th step: Constraints
    ///////////////////////////
    $("#srv_language_node").click(function () {
        $("#srv_language_node div.bs-actionsbox >div").removeClass('btn-block');
        //$("#srv_language_node div.bs-actionsbox > div >button:nth-child(2)").append('<i class="fa fa-remove text-danger"></i> ');
        $("#srv_language_node div.bs-actionsbox > div >button:eq(2)").append('<i class="fa fa-remove text-danger"></i> ');
    });

    // Handle the user response related to the geolocation constraints
    var geolocationBtn = new Swap2Buttons($("#srv_geolocation_y"), $("#srv_geolocation_n"));
    $("#srv_geolocation_y").click(function (event) { geolocationBtn.click($(this)); $(".srv_coordinates").removeClass('hidden'); });
    $("#srv_geolocation_n").click(function (event) { geolocationBtn.click($(this)); $(".srv_coordinates").addClass('hidden'); });

    // Handle the user response related to the language constraints
    var langBtn = new Swap2Buttons($("#srv_language_constraint_y"), $("#srv_language_constraint_n"));
    $("#srv_language_constraint_y").click(function (event) { langBtn.click($(this)); $("#srv_language_div").removeClass('hidden'); });
    $("#srv_language_constraint_n").click(function (event) { langBtn.click($(this)); $("#srv_language_div").addClass('hidden'); });


    //////////////////////////
    // 6th step: registration
    //////////////////////////
    $('#srv_terms').change(function () {
        if ($(this).is(':checked')) {
            $('#register-btn').removeClass('disabled');
            $('#update-btn').removeClass('disabled');
        };
        if ($(this).is(':checked') == false) {
            $('#register-btn').addClass('disabled');
            $('#update-btn').addClass('disabled');
        };
    });

    // handle tab selection
    $("ul#tabs > li").click(function (event) {
        if ($(this).hasClass('disabled')) { return false; }
        setPagers(parseInt($(this).find('a').attr('href').replace(/\D/g, '')));
    })



});


$(document).on('click', ".remove-kwd", function () {
    $(this).parent().remove();
})

$(document).on('change', "#srv_coverage", function () {
    getMap();
}).on('change', "#srv_latitude", function () {
    getMap();
}).on('change', "#srv_longitude", function () {
    getMap();
});


///////////////////////////
//      Logo
///////////////////////////

// Add a logo of the service
function addLogo() {
    $('#srv_logo').click();
    return false;
}

// Load the logo 
function loadLogo(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#thumbnail').attr('src', e.target.result);
            $('#thumbnail').parent().removeClass('hidden');
            $('#clear_thumbnail').removeClass('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Remove the existing logo of the service
function removeLogo() {
    $('#srv_logo').val('');
    $('#thumbnail').parent().addClass('hidden');
    $('#clear_thumbnail').addClass('hidden');
    return false;
}


///////////////////////////
//      Keywords
///////////////////////////

// Append keywords for the new service
function appendServiceKeyword() {
    var keyword = $("#srv_keyword").val().replace(/\s+/, '');

    if (keyword.length) {
        var tag = '<label class="label label-primary"><span class="fa fa-remove fa-fw remove-kwd cursor-pointer"></span> <span class="srv_keyword_list">' + keyword + '</span></label> ';
        $("#test").append(tag);

    //if (filterVal.length) {
        //$("#srv_keyword_list").append('<option value="' + $("#srv_keyword").val() + '" selected>' + $("#srv_keyword").val() + '</option>');
        $("#srv_keyword").val("");
    }
}

// Remove keywords of the new service
function removeServiceKeywords() {
    $("#srv_keyword_list :selected").each(function () {
        $(this).remove();
    });
}


///////////////////////////
//  Software package
///////////////////////////

// Add a package of the service
function addPackage() {
    $('#srv_software').click();
    return false;
}

// Load the package 
function loadPackage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#srv_software_info').text(input.files[0]["name"]);
            $('#srv_software_info').parent().removeClass('hidden');
            $('#clear_srv_software').removeClass('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Remove the existing logo of the service
function removePackage() {
    $('#srv_software').text('');
    $('#srv_software_info').parent().addClass('hidden');
    $('#clear_srv_software').addClass('hidden');
    return false;
}


///////////////////////////
//    Email wish list
///////////////////////////

// Send emails to wish list
function sendItemsWishList() {
    $("select#srv_email_list :selected").each(function () {
        $("select#srv_wish_list").append('<option value="' + $(this).attr("value") + '" selected>' + $(this).text() + '</option>');
        $(this).remove();
    });
}

// Remove emails from wish list
function removeItemsWishList() {
    $("select#srv_wish_list :selected").each(function () {
        $("select#srv_email_list").append('<option value="' + $(this).attr("value") + '">' + $(this).text() + '</option>');
        $(this).remove();
    });
}


////////////////////////////
//  Navigation
////////////////////////////

// Prevent click event on disabled tabs. 
// User can navigate in the wizard content using the previous/next buttons.
function preventClickTab(tab) {
    if ( tab.hasClass('disabled') ) {
        return false;
    }
    return true;
}

// Proceed to the content of the next Tab altering the view of both current and new Tab.
function nextStep() {
    var destination = $("#service-registration-wizard").find('li.active>a').attr("href");
    var currID = parseInt(destination.replace(/\D/g, ''));
    var newID = currID + parseInt(1);
    var next = "#step" + newID;

    if (newID <= 6) {
        if (wizardValidation(currID)) { 
            // change tab
            $('a[href="' + destination + '"]').parent().removeClass('active');
            $("#my-tab-content").find(destination).removeClass('active').removeClass('in');

            // load content of new tab
            $('a[href="' + next + '"]').parent().removeClass('disabled').addClass('active');
            $("#my-tab-content").find(next).addClass('active').addClass('in');
            $("#my-tab-content").find(next + '>div').animate("slow");

            // show previous btn

            setPagers(newID);

            if (newID == 4) {
                getMap();
            }
        }
    }
}

// Proceed to the content of the previous Tab altering the view of both current and new Tab.
function previousStep() {
    var destination = $("#service-registration-wizard").find('li.active>a').attr("href");
    var currID = parseInt(destination.replace(/\D/g, ''));
    var newID = currID - parseInt(1);
    var previous = "#step" + newID;

    if (newID >= 1) {
        if (wizardValidation(currID)) {
            $('a[href="' + destination + '"]').parent().removeClass('active');
            $("#my-tab-content").find(destination).removeClass('active').removeClass('in');

            $('a[href="' + previous + '"]').parent().removeClass('disabled').addClass('active');
            $("#my-tab-content").find(previous).addClass('active').addClass('in');

            setPagers(newID);
        }
    }
}

// Set pager state
function setPagers(id) {
    var step = { min: 1, max: 6 };

    switch(id){
        case step.min:
            $(".previous").addClass("hidden");
            $(".next").removeClass("hidden");
            return ;
        case step.max:
            $(".previous").removeClass("hidden");
            $(".next").addClass("hidden");
            return;
        default:
            $(".previous").removeClass("hidden");
            $(".next").removeClass("hidden");
    }
}



////////////////////////////
//  Validation
////////////////////////////

function wizardValidation(step) {
    // cases
    var validator = new ServiceRegistration(null);

    switch (step) {
        case 1:
            return validator.basicInformationTab();
        case 2:
            return validator.chargingTab();
        case 3:
            return validator.usageTab();
        case 4:
            return validator.constraintsTab();
        case 5:
            return validator.supportTab();
        case 6:
            return validator.confirmTab();
        default:
            return false;
    }
}


////////////////////
//      Map        
////////////////////

// Initialize map

function getMap() {
    // Initiate variables
    var lat = ($("#srv_latitude").val() === "") ? 39.0 : $("#srv_latitude").val();
    var lng = ($("#srv_longitude").val() === "") ? 22.0 : $("#srv_longitude").val();

    // Initiate coordinates
    var coordinates = new google.maps.LatLng(lat, lng);
    // Set options
    var mapOptions = {
        zoom: 8,
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
    var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    var marker = new google.maps.Marker({
        position: coordinates,
        map: map,
        draggable: true
    });

    var radius = ($("#srv_coverage").val() === undefined) ? 0 : $("#srv_coverage").val() * 1000;
    var area = new google.maps.Circle({
        strokeColor: 'red',
        strokeOpacity: 0.8,
        fillColor: '#AAAAAA',
        fillOpacity: 0.4,
        strokeWeight: 2,
        map: map,
        center: coordinates,
        radius: radius
    });

    // Handle user actions
    google.maps.event.addListener(marker, 'click', function (event) {
        new setCoordinates(event, radius, map);
    });
    google.maps.event.addListener(marker, 'dragend', function (event) {
        new setCoordinates(event, radius, map);
    });
    // Set marker in center
    map.setCenter(marker.position);
    marker.setMap(map);
}

// Set the coordinates
function setCoordinates(event, radius, map) {
    $("#srv_latitude").val(event.latLng.lat().toFixed(4));
    $("#srv_longitude").val(event.latLng.lng().toFixed(4));

    var circle = new google.maps.Circle({
        strokeColor: 'red',
        strokeOpacity: 0.8,
        fillColor: '#AAAAAA',
        fillOpacity: 0.4,
        strokeWeight: 2,
        map: map,
        center: new google.maps.LatLng(event.latLng.lat().toFixed(4), event.latLng.lng().toFixed(4)),
        radius: radius
    });
}

//////////////////////
//  Submit service
//////////////////////
$("#register-btn").click(function (event) {
    event.preventDefault();

    var url = $(this).data().url;
    var mediaURL = url + "/media/upload/"
    var form = $("#insert-new-service");
    var payload = collectControlData(form);
    var files = new FormData($("#insert-new-service")[0]);

    var loading = new AjaxView(form);
    loading.show();
    $.ajax({
        type: 'POST',
        url: url,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        data: JSON.stringify(payload),
        success: function (response) {
            if (response.state === true) {
                // media
                $.ajax({
                    type: 'POST',
                    url: mediaURL + response.id,
                    data: files,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.state === true) {
                            setTimeout(function () {
                                loading.hide();
                                //window.location.href = response.link;
                                window.location.href = "/offerings";
                            }, 600);
                        }
                    },
                    error: function () {
                    }
                });
            }
        },
        error: function (response) {
            console.error(response);
        },
        complete: function () {
        }
    });
    return false;
});



//////////////////////
//  Update service 
//////////////////////

// Load the user option in edit mode of service
function crowdPartState(state) {
    if (state === "True") {
        $("#srv_availability_pb").click();
    }
    else {
        $("#srv_availability_pr").click();
    }
}

function langBtnState(state) {
    if (state === "True") {
        $("#srv_language_constraint_y").click();
        return;
    }
    $("#srv_language_constraint_n").click();
}

function geolocationBtnState(state) {
    if (state === "True") {
        $("#srv_geolocation_y").click();
        return;
    }
    $("#srv_geolocation_n").click();
}

$("#update-btn").click(function (event) {
    event.preventDefault();
    var form = $("#insert-new-service");
    var payload = collectControlData(form);
    var url = $(this).data().url;
    var mediaURL = "/offerings/services/media/upload/";
    var files = new FormData(form[0]);

    var loading = new AjaxView($("#service-registration-wizard"));
    loading.show();
    $.ajax({
        type: 'PUT',
        url: url,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        data: JSON.stringify(payload),
        success: function (response) {
            if (response.state === true) {
                // media
                $.ajax({
                    type: 'POST',
                    url: mediaURL + response.id,
                    data: files,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        if (response.state === true) {
                            setTimeout(function () {
                                loading.hide();
                                window.location.href = response.link;
                            }, 600);
                        }
                    },
                    error: function () {
                    }
                });
            }
        },
        error: function (response) {
            alert("An error is occured. The service modification failed");
        },
        complete: function (response) {
        }
    });
    return false;
});

function collectControlData(form) {
    var data = form.serializeArray();
    var payload = {};

    // Convert array of objects to object (JSON payload)
    for (var i in data) {
        payload[data[i]["name"]] = data[i]["value"]
    }

    payload["srv_category"] = $("#srv_category").val();
    payload["srv_language_constraint"] = ($("#srv_language_constraint").find("a.btn-primary").attr("id") == 'srv_language_constraint_y') ? 1 : 0;
    payload["availability"] = ($("#srv_availability").find("a.btn-primary").attr("id") == 'srv_availability_pb') ? 1 : 0;
    payload["srv_geolocation"] = ($("#srv_geolocation").find("a.btn-primary").attr("id") == 'srv_geolocation_y') ? 1 : 0;
    if (!payload["srv_geolocation"]) {
        payload['srv_latitude'] = 0.0;
        payload['srv_longitude'] = 0.0;
        payload['srv_coverage'] = 0;
    }
    // keywords
    payload["srv_keywords"] = []
    //$("#srv_keyword_list >option").each(function (i) {
    //    var keyword = $(this).attr("value");
    //    if (i != 0) {
    //        payload["srv_keywords"][i] = keyword;
    //    }
    //})
    $(".srv_keyword_list").each(function (i) {
        payload["srv_keywords"][i] = $(this).text();
    });

    // language constraint: null if no constraint
    payload["srv_language"] = []
    $("#srv_language >option:selected").each(function (i) {
        var language = $(this).attr("value");
        if (language !== null) {
            payload["srv_language"][i] = language;
        }
    })
    // terms accepted or not
    payload["srv_terms"] = $("#srv_terms").prop('checked');

    return payload;
}


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});