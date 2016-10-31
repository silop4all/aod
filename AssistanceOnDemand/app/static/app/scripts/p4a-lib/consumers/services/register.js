
google.maps.event.addDomListener(window, 'load', getMap);

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

var crowdPartBtn = null;
var langBtn = null;
var geolocationBtn = null;

$(document).ready(function () {
    //
    // Set the links of the steps as inactive
    //
    $("ul#tabs > li").click(function (event) {
        if ($(this).hasClass('disabled')) { return false; }
        setPagers(parseInt($(this).find('a').attr('href').replace(/\D/g, '')));
    })
    //
    // Load the categories in tree view
    //
    var loading = new AjaxView($("#BasicServiceForm"));
    loading.show();
    $.ajax({
        type: 'GET',
        url: $("#categories").data('resource'),
        data: { level: 0 },
        headers: { "accept": "application/json", "content-type": "application/json" },
        contentType: 'application/json',
        success: function (response) {
            //
            // Load categories and display them as a tree
            //
            var options = '';
            var data = response.results;
            for (var root in data) {
                options += '<optgroup label="' + data[root].title + '">';
                var childs = data[root].children;
                for (var i in childs) {
                    options += '<option value="' + childs[i].id + '" title="' + childs[i].title + '">' + childs[i].title + ' </option>';

                    var leafs = childs[i].children;
                    for (var j in leafs) {
                        options += '<option data-content="<span class=\'padding-left-20\'>  ' + leafs[j].title + '</span>" data-icon="fa fa-minus" value="' + leafs[j].id + '">' + leafs[j].title + '</option>';
                    }
                }
                options += '</optgroup>';
            }
            $("#categories").append(options);
            $("#categories").selectpicker('refresh');
        },
        error: function (response) {
            console.error(response);
        },
        complete: function () {
            //
            // Load selected categories in edit mode
            //
            if (typeof (selectedCategories) !== "undefined") {
                $('#categories').selectpicker('val', selectedCategories);
            }
            //
            // Format the root categories located in optgroups 
            //
            $("ul.selectpicker > li > span").css('color', "black").css('font-size', "18px").css("font-weight", "bold");
            loading.hide();
        }
    });
    //
    // Initialize variables
    //
    crowdPartBtn = new Swap2Buttons($("#availability_pb"), $("#availability_pr"));
    langBtn = new Swap2Buttons($("#language_constraint_yes"), $("#language_constraint_no"));
    geolocationBtn = new Swap2Buttons($("#location_constraint_yes"), $("#location_constraint_no"));
    //
    // Load selected languages in edit mode
    //
    if (typeof (selectedLanguages) !== "undefined") {
        $('#languages').selectpicker();
        $('#languages').selectpicker('val', selectedLanguages);
    }

}).on('click', "div#service-registration-wizard > div > ul > li", function () {
    //
    // Prevent click event on disabled tabs. 
    //
    return preventClickTab($(this));
}).on('change', '#type', function () {
    //
    // Hide or display optional fields in Basic tab
    //
    if ($(this).val() === "H") {
        $("#version_input").addClass("hidden");
        $("#license_input").addClass("hidden");
    }
    if ($(this).val() === "M") {
        $("#version_input").removeClass("hidden");
        $("#license_input").removeClass("hidden");
    }
}).on(
    'click', "#load_image", addLogo
).on('change', "#image", function () {
    //
    // load image
    //
    loadLogo(this);
}).on("change", "#charging_policy", function () {
    //
    // actions on charging policy change
    //
    if ($("#charging_policy :selected").attr('value') == "1") {
        $("#price").val('0.00').attr('readonly', true);
        $("#price").parent().removeClass("has-error");
        $("#unit").attr('readonly', true);
    }
    else {
        $("#price").val('').removeAttr('readonly', false);
        $("#unit").removeAttr('readonly', false);
    }
}).on('click', "#availability_pb", function (event) {
    //
    // hide select boxes
    //
    crowdPartBtn.click($(this));
    $("#set_target_users").addClass('hidden');
}).on('click', "#availability_pr", function (event) {
    //
    // show select boxes
    //
    crowdPartBtn.click($(this));
    $("#set_target_users").removeClass('hidden');
}).on(
    'click', "#send_to_wish_list", sendItemsWishList
).on(
    'click', "#send_to_email_list", removeItemsWishList
).on('click', "#language_node", function () {
    //
    //  
    //
    $("#language_node div.bs-actionsbox >div").removeClass('btn-block');
    $("#language_node div.bs-actionsbox > div >button:eq(2)").append('<i class="fa fa-remove text-danger"></i> ');
}).on('click', "#location_constraint_yes", function (event) {
    //
    // Display map and related fields
    //
    geolocationBtn.click($(this));
    $(".srv_coordinates").removeClass('hidden');
}).on('click', "#location_constraint_no", function (event) {
    //
    // Hide map and related fields
    //
    geolocationBtn.click($(this));
    $(".srv_coordinates").addClass('hidden');
}).on('click', "#language_constraint_yes", function (event) {
    //
    // Display languages drop-down list
    //
    langBtn.click($(this));
    $("#language_div").removeClass('hidden');
}).on('click', "#language_constraint_no", function (event) {
    //
    // Hide languages drop-down list
    //
    langBtn.click($(this));
    $("#language_div").addClass('hidden');
}).on(
    'change', "#coverage", getMap
).on(
    'change', "#latitude", getMap
).on(
    'change', "#longitude", getMap
).on('change', '#terms', function () {
    if ($(this).is(':checked')) {
        $('#register-btn').removeClass('disabled');
        $('#update-btn').removeClass('disabled');
    };
    if ($(this).is(':checked') === false) {
        $('#register-btn').addClass('disabled');
        $('#update-btn').addClass('disabled');
    };
}).on('click', "#register-btn", function (event) {
    AoD.validateConfirmServiceForm("#ConfirmServiceForm");
}).on('click', "#update-btn", function (event) {
    AoD.validateConfirmServiceForm("#ConfirmServiceForm");
});


function addLogo() {
    //
    // Simulate the click event on input 
    //
    $('#image').click();
    return false;
}

function loadLogo(input) {
    //
    // Load a new logo for the service
    //
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#thumbnail').attr('src', e.target.result);
            $('#thumbnail').removeClass('hidden');
            $('#thumbnail').parent().removeClass('hidden');
            $('#clear_thumbnail').removeClass('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function removeLogo() {
    //
    // Remove the existing logo of the service
    //
    $('#image').val('');
    $('#thumbnail').parent().addClass('hidden');
    $('#clear_thumbnail').addClass('hidden');
    return false;
}

function wizardValidation(step) {
    var form = null;
    switch (step) {
        case 1:
            form = "#BasicServiceForm";
            AoD.validateBasicServiceForm(form);
            return $(form).valid();
        case 2:
            form = "#PaymentServiceForm";
            AoD.validatePaymentServiceForm(form);
            return $(form).valid();
        case 3:
            form = "#UsageServiceForm";
            AoD.validateUsageServiceForm(form);
            return $(form).valid();
        case 4:
            form = "#ConstraintsServiceForm";
            AoD.validateConstraintsServiceForm(form);
            return $(form).valid();
        case 5:
            form = "#SupportServiceForm";
            AoD.validateSupportServiceForm(form);
            return $(form).valid();
        case 6:
            form = "#ConfirmServiceForm";
            AoD.validateConfirmServiceForm(form);
            return $(form).valid();
        default:
            return false;
    }
}

function nextStep() {
    //
    // Proceed to the content of the next Tab altering the view of both current and new Tab.
    //
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
                //
                // Load google map
                //
                getMap();
            }
        }
    }
}

function previousStep() {
    //
    // Proceed to the content of the previous Tab altering the view of both current and new Tab.
    //
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

function setPagers(id) {
    //
    // Set pager state
    //
    var step = { min: 1, max: 6 };

    switch (id) {
        case step.min:
            $(".previous").addClass("hidden");
            $(".next").removeClass("hidden");
            return;
        case step.max:
            $(".previous").removeClass("hidden");
            $(".next").addClass("hidden");
            return;
        default:
            $(".previous").removeClass("hidden");
            $(".next").removeClass("hidden");
    }
}

function preventClickTab(tab) {
    // Prevent click event on disabled tabs.
    // User can navigate in the wizard content using the previous/next buttons.
    if (tab.hasClass('disabled')) {
        return false;
    }
    return true;
}

function crowdPartState(state) {
    //
    // Load the scope of the service (public or limited access)
    //
    if (state === "True") {
        $("#availability_pb").click();
    }
    else {
        $("#availability_pr").click();
    }
}

function sendItemsWishList() {
    //
    // Send emails to wish list
    //
    $("select#srv_email_list :selected").each(function () {
        $("select#srv_wish_list").append('<option value="' + $(this).attr("value") + '" selected>' + $(this).text() + '</option>');
        $(this).remove();
    });
}

function removeItemsWishList() {
    //
    // Remove emails from wish list
    //
    $("select#srv_wish_list :selected").each(function () {
        $("select#srv_email_list").append('<option value="' + $(this).attr("value") + '">' + $(this).text() + '</option>');
        $(this).remove();
    });
}

function langBtnState(state) {
    //
    // Load the state of lingual constraint
    //
    if (state === "True") {
        $("#language_constraint_yes").click();
        return;
    }
    $("#language_constraint_no").click();
}

function geolocationBtnState(state) {
    //
    // Load the state of locational constraints
    //
    if (state === "True") {
        $("#location_constraint_yes").click();
        return;
    }
    $("#location_constraint_no").click();
}

function getMap() {
    //
    // Initialize map
    //
    var lat = ($("#latitude").val() === "") ? 39.0 : $("#latitude").val();
    var lng = ($("#longitude").val() === "") ? 22.0 : $("#longitude").val();

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

    var radius = ($("#coverage").val() === undefined) ? 0 : $("#coverage").val() * 1000;
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

function setCoordinates(event, radius, map) {
    //
    // Set the coordinates
    //
    $("#latitude").val(event.latLng.lat().toFixed(4));
    $("#longitude").val(event.latLng.lng().toFixed(4));

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

function openTermsWindow() {
    //
    // Pop up window that contains the Terms of usage for services in platform
    //
    swal({
        title: gettext("Terms of usage"),
        text: gettext("Terms of usage content..."),
        type: "info",
        confirmButtonText: gettext("Ok, I understood"),
        confirmButtonColor: "#3a87ad",
        animation: "slide-from-top"
    });
}
