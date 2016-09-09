var form = '#service-search-form';

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

$(document).ready(function () {
    // get categories as a tree
    getCategories();

    $("#companies-id").click(function () {
        toggleArrows($(this));
    });

    $("#categories-id").click(function () {
        toggleArrows($(this));
    });

    $("#service-types-id").click(function () {
        toggleArrows($(this));
    });

    $("#service-price-id").click(function () {
        toggleArrows($(this));
    });

    $("#location-id").click(function () {
        toggleArrows($(this));
    });

    $("#quality-of-service-id").click(function () {
        toggleArrows($(this));
    });

    $(".rating-stars").click(function () {
        swapRatingStarColor($(this).attr("id").match(/\d+/));

    });
    $(".rating-stars").hover(function () {
        swapRatingStarColor($(this).attr("id").match(/\d+/));
    });

    /////////////////
    // Add shadow on service banners if mouse enters. Else, remove shadow
    /////////////////
    $(".on-mouseover > div").mouseenter(function () {
        $(this).addClass("highlight-service-banner");
    }).mouseleave(function () {
        $(this).removeClass("highlight-service-banner");
    });

    /////////////////
    // Set the stars of any service based on its rating value
    /////////////////
    $(".service-banner").each(function () {
        var rating = $(this).find("#srv-rating-" + $(this).attr("id").match(/\d+/)).find("span").first().text();
        if (rating !== "None" && !(isNaN(rating))) {
            for (var j = 1; j <= Math.ceil(rating) ; j++) {
                $(this).find(".star-rating-" + j).removeClass("fa-star-o").addClass("fa-star");
            }
        }
    });


    ////////////////////////////////////
    // Services per page
    ////////////////////////////////////
    $("#items-per-page-id").change(function () {
        var params = getUrlparameters();
        params["limit"] = $(this).find(":selected").val();
        var delimeter = '?';

        var url = '';
        for (var j in params) {
            url += delimeter + j + '=' + params[j]
            delimeter = '&';
        }
        // window.location.href = url;
    });

    ////////////////////////////////////
    // Handle the sorting of services
    ////////////////////////////////////
    $(".my-sort-choice").change(function () {
        var params = getUrlparameters();
        params["sortby"] = $(this).find("select").val();
        /*
        var delimeter = '?';

        var url = '';
        for (var j in params){
            url += delimeter+j+'='+params[j]
            delimeter = '&';
        }
        window.location.href = url;
        */
        $("#sortby").data().sort = $(this).find("select").val();
        reload($(this).find("select").val(), $(".services-view").data().view);
    });

    ////////////////////////////////////
    // Filter all services by type (H/M/All)
    ////////////////////////////////////
    $("div#service-types-list > div > div").change(function () {
        var type = $(this).find("input").attr("id");
        var params = getUrlparameters();
        params["type"] = type[0].toUpperCase();
        var delimeter = '?';

        var url = '';
        for (var j in params) {
            url += delimeter + j + '=' + params[j]
            delimeter = '&';
        }
        //window.location.href = url;
    });


    ///////////////////////////////////
    // Filter services by charging model
    ///////////////////////////////////
    $("div#charging-model-list > div > div").change(function () {
        var model = $(this).find("input").attr("id").match(/\d+/);
        var params = getUrlparameters();
        params["model"] = model[0];
        var delimeter = '?';

        var url = '';
        for (var j in params) {
            url += delimeter + j + '=' + params[j]
            delimeter = '&';
        }
        // window.location.href = url;
    });


    //////////////////////////
    // Keep selected the sort_by user choice
    //////////////////////////
    $("#content-top-banner").find("#sortby :selected").prop('selected', false);
    //$("#sortby option[value='{{ sortby }}']").attr('selected', 'selected');
    $("#sortby option[value='"+sortby+"']").attr('selected', 'selected');


    //////////////////////////
    //  Keep limit user choice
    //////////////////////////
    $("#content-top-banner").find("#items-per-page-id :selected").prop('selected', false);
    //$("#items-per-page-id option[value='{{ limit }}']").attr('selected', 'selected');
    $("#items-per-page-id option[value='" + limit + "']").attr('selected', 'selected');

}).on('click', "#search-btn", function (event) {
    event.preventDefault();
    
    var search = {
        owners: [],
        categories: [],
        types: [],
        models: [],
        minPrice: null,
        maxPrice: null,
        distance: null,
        lat: null, 
        lon: null,
        minQoS: null,
        maxQoS: null,
        sortby: $("#sortby").data().sort,
        view: $(".services-view").data().view
    }

    // get list of owner(s)
    $("div#companies-id").find('input:checked').each(function(i){
        search.owners.push($(this).data().id);
    });
    // categories
    $("div#categories-id").find('input:checked').each(function(i){
        search.categories.push($(this).data().id);
    });
    // types
    $("div#service-types-id").find('input:checked').each(function (i) {
        search.types.push($(this).data().id);
    });
    // charging model
    $("div#charging-model-id").find('input:checked').each(function (i) {
        search.models.push($(this).data().id);
    });
    // price
    search.minPrice = $("#low_price").val();
    search.maxPrice = $("#high_price").val();
    if (search.minPrice < 0 || search.maxPrice < 0) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The price values must be non negative numbers!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minPrice > search.maxPrice) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The maximum price value must be greater than (or equal with) the minimum one!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    
    // QoS
    if ($("#low_QoS").val() !== "") {
        search.minQoS = $("#low_QoS").val();
    };
    if ($("#high_QoS").val() !== ""){
        search.maxQoS = $("#high_QoS").val();
    }   
    if (search.minQoS < 0 || search.minQoS > 5) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The minimum value of Quality of Service field is out of range. Please enter a value in range [0,5]!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.maxQoS < 0 || search.maxQoS > 5) {
        swal({
            html: false,
            title: "Invalid input",
            text: "The maximum value of Quality of Service field is out of range. Please enter a value in range [0,5]!",
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minQoS > search.maxQoS) {
        swal({
            html: false,
            title: "Invalid input",
            text: "The maximum value of Quality of Service field must be greater than (or equal with) the corresponding minimum one!",
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }


    // distance threshold
    search.distance = $("div#location-id").find('input').val();
    if (search.distance < 0) {
        swal({
            html: false,
            title: "Invalid input",
            text: "The distance value must be a non negative number. Keep in mind that this value maps to kilometers.",
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    // inform user for location tracking
    if (search.distance !== "") {
        swal({
            html: false,
            title: "AoD message",
            text: "The AoD platform wants your permission to track your location. Do you agree with this action?",
            type: "info",
            showCancelButton: true,
            confirmButtonClass: "btn-primary",
            confirmButtonText: "Yes, I agree!",
            cancelButtonText: "No, I do not agree!",
            cancelButtonClass: "btn-danger",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (isConfirm) {
                swal({
                    html: false,
                    title: "Search progress",
                    text: "AoD scans the services that meet your requirements",
                    type: "success",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "btn-primary",
                });
            } else {
                swal({
                    html: false,
                    title: "Search progress",
                    text: "The service searching was aborted.",
                    type: "warning",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "#d9534f"
                });
            }
        });

    }

    // get user coordinates
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            console.log(parseFloat(position.coords.latitude));
            console.log(parseFloat(position.coords.longitude));
            //search.lat = parseFloat(position.coords.latitude);
            //search.lon = parseFloat(position.coords.longitude);  
        })
    }
    search.lat = 49.602235199999996;
    search.lon = 6.1337418999999995;
    console.info(search);
    

    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        dataType: 'html',
        //cache: false,
        data: JSON.stringify(search),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (data) {
            $("#services-result").empty();
            $("#services-result").append(data);
        }
    });

}).on("click", "#charging-model-1", function () {
    if ($(this).is(':checked')) {
        if (!$("#charging-model-0").is(':checked')) {
            $("#low_price").attr('readonly', true).val('');
            $("#high_price").attr('readonly', true).val('');
        }
        else {
            $("#low_price").attr('readonly', false);
            $("#high_price").attr('readonly', false);
        }
    }
    else {
        $("#low_price").attr('readonly', false);
        $("#high_price").attr('readonly', false);
    }

}).on("click", "#charging-model-0", function () {
    if ($(this).is(':checked')) {
        $("#low_price").attr('readonly', false);
        $("#high_price").attr('readonly', false);
    }
    else {
        if ($("#charging-model-1").is(':checked')) {
            $("#low_price").attr('readonly', true).val('');
            $("#high_price").attr('readonly', true).val('');
        }
        else {
            $("#low_price").attr('readonly', false);
            $("#high_price").attr('readonly', false);
        }
    }
});


//////////////////////////////////
//  Parse URL and get the query parameters
//////////////////////////////////
function getUrlparameters() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
        function (m, key, value) {
            vars[key] = value;
        });
    return vars;
}

// get the new URL
function getURL(url, sort_by, srv_type, limit) {
    if (srv_type === null) {
        return url + "?sortby=" + sort_by + "&limit=" + limit;
    }
    else {
        return url + "?type=" + srv_type + "&sortby=" + sort_by + "&limit=" + limit;;
    }
    return request;
}


////////////////////////////////////
//  Swap the state of rating stars
////////////////////////////////////
function swapRatingStarColor(index) {
    var min = 1, max = 6;
    for (var j = min; j < max; j++) {
        if (j > index) {
            $("#rating-star-" + j).removeClass("fa-star").addClass("fa-star-o");
        }
        else {
            $("#rating-star-" + j).removeClass("fa-star-o").addClass("fa-star");
        }

    }
}

//////////////////////////////////////////
//  Swap the direction of search engine
//////////////////////////////////////////
function toggleArrows(element) {
    if (element.find(" .panel-collapse").hasClass("in")) {
        element.find("i").removeClass("fa-angle-double-down").addClass("fa-angle-double-up");
    }
    else {
        element.find("i").addClass("fa-angle-double-down").removeClass("fa-angle-double-up");
    }

}


//////////////////////////////
// Declare and load view
/////////////////////////////
$("#list_view").click(function () {
    var params = getUrlparameters();
    params["view"] = 'l';
    var delimeter = '?';

    var url = '';
    for (var j in params) {
        url += delimeter + j + '=' + params[j]
        delimeter = '&';
    }
    //window.location.href = url;
    //update(url);

    $(".services-view").data().view = 'l';
    reload($("#sortby").data().sort, 'l');
});
$("#multidata_view").click(function () {
    var params = getUrlparameters();
    params["view"] = 'm';
    var delimeter = '?';

    var url = '';
    for (var j in params) {
        url += delimeter + j + '=' + params[j]
        delimeter = '&';
    }
    //window.location.href = url;
    //update(url);

    $(".services-view").data().view = 'm';
    reload($("#sortby").data().sort, 'm');
});

//function update(url) {
//    var u = url.replace("/index", '');
//    alert(u);
//    $.ajax({
//        type: 'GET',
//        url: "/services/search" + u,
//        dataType: 'html',
//        beforeSend: function (xhr, settings) {
//            $.ajaxSettings.beforeSend(xhr, settings);
//        },
//        success: function (data) {
//            $("#services-result").empty();
//            $("#services-result").append(data);
//        }
//    });
//}



function reload(sortby, view) {
    event.preventDefault();

    var search = {
        owners: [],
        categories: [],
        types: [],
        models: [],
        minPrice: null,
        maxPrice: null,
        distance: null,
        lat: null,
        lon: null,
        minQoS: null,
        maxQoS: null,
        sortby: sortby,
        view: view
    }

    // get list of owner(s)
    $("div#companies-id").find('input:checked').each(function (i) {
        search.owners.push($(this).data().id);
    });
    // categories
    $("div#categories-id").find('input:checked').each(function (i) {
        search.categories.push($(this).data().id);
    });
    // types
    $("div#service-types-id").find('input:checked').each(function (i) {
        search.types.push($(this).data().id);
    });
    // charging model
    $("div#charging-model-id").find('input:checked').each(function (i) {
        search.models.push($(this).data().id);
    });
    // price
    search.minPrice = $("#low_price").val();
    search.maxPrice = $("#high_price").val();
    if (search.minPrice < 0 || search.maxPrice < 0) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The price values must be non negative numbers!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minPrice > search.maxPrice) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The maximum price value must be greater than (or equal with) the minimum one!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }

    // QoS
    if ($("#low_QoS").val() !== "") {
        search.minQoS = $("#low_QoS").val();
    };
    if ($("#high_QoS").val() !== "") {
        search.maxQoS = $("#high_QoS").val();
    }
    if (search.minQoS < 0 || search.minQoS > 5) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The minimum value of Quality of Service field is out of range. Please enter a value in range [0,5]!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.maxQoS < 0 || search.maxQoS > 5) {
        swal({
            html: false,
            title: "Invalid input",
            text: 'The maximum value of Quality of Service field is out of range. Please enter a value in range [0,5]!',
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minQoS > search.maxQoS) {
        swal({
            html: false,
            title: "Invalid input",
            text: "The maximum value of Quality of Service field must be greater than (or equal with) the corresponding minimum one!",
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }


    // distance threshold
    search.distance = $("div#location-id").find('input').val();
    if (search.distance < 0) {
        swal({
            html: false,
            title: "Invalid input",
            text: "The distance value must be a non negative number. Keep in mind that this value maps to kilometers.",
            type: "warning",
            confirmButtonText: "Continue",
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    // inform user for location tracking
    if (search.distance !== "") {
        swal({
            html: false,
            title: "AoD message",
            text: "The AoD platform wants your permission to track your location. Do you agree with this action?",
            type: "info",
            showCancelButton: true,
            confirmButtonText: "Yes, I agree!",
            confirmButtonColor: "btn-primary",
            cancelButtonText: "No, I do not agree!",
            cancelButtonColor: "btn-danger",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (isConfirm) {
                swal({
                    html: false,
                    title: "Search progress",
                    text: "AoD scans the services that meet your requirements",
                    type: "success",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "btn-primary",
                });
            } else {
                swal({
                    html: false,
                    title: "Search progress",
                    text: "The service searching was aborted.",
                    type: "warning",
                    confirmButtonText: "Continue",
                    confirmButtonColor: "#d9534f"
                });
            }
        });
    }
    // get user coordinates
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            console.log(parseFloat(position.coords.latitude));
            console.log(parseFloat(position.coords.longitude));
            //search.lat = parseFloat(position.coords.latitude);
            //search.lon = parseFloat(position.coords.longitude);  
        })
    }

    search.lat = 37.9902181;
    search.lon = 23.7608382;
    console.info(search);


    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        dataType: 'html',
        //cache: false,
        data: JSON.stringify(search),
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (data) {
            $("#services-result").empty();
            $("#services-result").append(data);
        }
    });
}


function getCategories() {

    $.ajax({
        type: 'GET',
        url: $('#tree').data('resource'),
        data: { level: 0 },
        headers: { "accept": "application/json", "content-type": "application/json" },
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        contentType: 'application/json',
        success: function (response) {
            var options = '';
            var data = response.results;
            
            var startList = '<ul><li>';
            var startListInvisible = '<ul><li class="collapsed">';
            var endList = '</li></ul>';
            for (var root in data) {
                var childs = data[root].children;

                options += [
                    ((childs.length > 0) ? startListInvisible : startList),
                    '<input type="checkbox" id="category-' + data[root].id + '" name="category-'+data[root].id+'" data-id="'+data[root].id+'" data-name="category-'+data[root].id+'"/>',
                    '<span for="category-' + data[root].id + '"> <strong>' + data[root].title + '</strong></span>',
                ].join('');

                
                for (var i in childs) {
                    var leafs = childs[i].children;
                    options += [
                        ((leafs .length> 0) ? startListInvisible : startList),
                        '<input type="checkbox" id="category-' + childs[i].id + '" name="category-' + childs[i].id + '" data-id="' + childs[i].id + '" data-name="category-' + childs[i].id + '"/>',
                        '<span for="category-' + childs[i].id + '"> ' + childs[i].title + '</span>',
                    ].join('');

                    
                    for (var j in leafs) {
                        options += [
                            startList,
                                '<input type="checkbox" id="category-' + leafs[j].id + '" name="category-' + leafs[j].id + '" data-id="' + leafs[j].id + '" data-name="category-' + leafs[j].id + '"/>',
                                    '<span for="category-' + leafs[j].id + '"> ' + leafs[j].title + '</span>',
                            endList
                        ].join('');
                    }
                    options += endList;
                }
                options += endList;
            }
            $('#tree').append(options);
            $('#tree').tree({
                collapsible: true,
                dnd: false,
                onCheck: {
                    node: 'expand'
                },
                onUncheck: {
                    node: 'collapse'
                }
            });
            $('#tree').css('border', 'none');
            $(".daredevel-tree-anchor").css("margin-top", '4px');

        },
        error: function (response) {
            console.error(response);
        },
        complete: function () {
        }
    });

}