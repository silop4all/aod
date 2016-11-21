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
    getResults(form, null);

    $(".panel-toggle-arrows").click(function () {
        toggleArrows($(this));
    });


    $(".rating-stars").click(function () {
        swapRatingStarColor($(this).attr("id").match(/\d+/));

    });
    $(".rating-stars").hover(function () {
        swapRatingStarColor($(this).attr("id").match(/\d+/));
    });
    //
    // Services per page
    //
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
    //
    // Handle the sorting of services
    //
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

    //
    // Filter all services by type (H/M/All)
    //
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

    //
    // Filter services by charging model
    //
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
    //
    // Keep selected the sort_by user choice
    //
    $("#content-top-banner").find("#sortby :selected").prop('selected', false);
    //$("#sortby option[value='{{ sortby }}']").attr('selected', 'selected');
    $("#sortby option[value='" + sortby + "']").attr('selected', 'selected');

    //
    //  Keep limit user choice
    //
    $("#content-top-banner").find("#items-per-page-id :selected").prop('selected', false);
    //$("#items-per-page-id option[value='{{ limit }}']").attr('selected', 'selected');
    $("#items-per-page-id option[value='" + limit + "']").attr('selected', 'selected');

}).on('click', "#search-btn", function (event) {
    event.preventDefault();

    var request = "";

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
        sortby: $("#sortby").val(),//$("#sortby").data().sort,
        view: $(".services-view").data().view
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
            title: gettext("Invalid input"),
            text: gettext('The price values must be non negative numbers!'),
            type: "warning",
            confirmButtonText: gettext("Continue"),
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minPrice > search.maxPrice) {
        swal({
            html: false,
            title: gettext("Invalid input"),
            text: gettext('The maximum price value must be greater than (or equal with) the minimum one!'),
            type: "warning",
            confirmButtonText: gettext("Continue"),
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
            title: gettext("Invalid input"),
            text: gettext('The minimum value of Quality of Service field is out of range. Please enter a value in range [0,5]!'),
            type: "warning",
            confirmButtonText: gettext("Continue"),
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.maxQoS < 0 || search.maxQoS > 5) {
        swal({
            html: false,
            title: gettext("Invalid input"),
            text: gettext("The maximum value of Quality of Service field is out of range. Please enter a value in range [0,5]!"),
            type: "warning",
            confirmButtonText: gettext("Continue"),
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    if (search.minQoS > search.maxQoS) {
        swal({
            html: false,
            title: gettext("Invalid input"),
            text: gettext("The maximum value of Quality of Service field must be greater than (or equal with) the corresponding minimum one!"),
            type: "warning",
            confirmButtonText: gettext("Continue"),
            confirmButtonColor: "#d9534f"
        });
        return;
    }


    // distance threshold
    search.distance = $("div#location-id").find('input').val();
    if (search.distance < 0) {
        swal({
            html: false,
            title: gettext("Invalid input"),
            text: gettext("The distance value must be a non negative number. Keep in mind that this value maps to kilometers."),
            type: "warning",
            confirmButtonText: gettext("Continue"),
            confirmButtonColor: "#d9534f"
        });
        return;
    }
    // inform user for location tracking
    if (search.distance !== "") {
        swal({
            html: false,
            title: gettext("AoD message"),
            text: gettext("The AoD platform wants your permission to track your location. Do you agree with this action?"),
            type: "info",
            showCancelButton: true,
            confirmButtonClass: "btn-primary",
            confirmButtonText: gettext("Yes, I agree!"),
            cancelButtonText: gettext("No, I do not agree!"),
            cancelButtonClass: "btn-danger",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {
            if (isConfirm) {
                swal({
                    html: false,
                    title: gettext("Search progress"),
                    text: gettext("AoD scans the services that meet your requirements"),
                    type: "success",
                    confirmButtonText: gettext("Continue"),
                    confirmButtonColor: "btn-primary",
                });
            } else {
                swal({
                    html: false,
                    title: gettext("Search progress"),
                    text: gettext("The service searching was aborted."),
                    type: "warning",
                    confirmButtonText: gettext("Continue"),
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
            search.lat = parseFloat(position.coords.latitude);
            search.lon = parseFloat(position.coords.longitude);  
        })
    }
    //search.lat = 49.602235199999996;
    //search.lon = 6.1337418999999995;
    console.info(search);

    //var request = "";
    //for (var q in search) {
    //    request += q;
    //    request += "=";
    //    request += (search.q === []) ? null : search.q;
    //    request += "&";
    //    console.log(q + " --> " + typeof (search.q));
    //    console.info("");
    //}
    getResults(form, search);

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
}).on("mouseenter", ".on-mouseover > div", function () {
    //
    // Highlight service box
    //
    $(this).addClass("highlight-service-banner");
}).on("mouseleave", ".on-mouseover > div", function () {
    //
    // Skip highlight from service box
    //
    $(this).removeClass("highlight-service-banner");
}).on('click', "#list_view", function () {
    //
    // Services in block view
    // 
    $("#services-result-listview").removeClass('hidden');
    $("#services-result-multidata").addClass('hidden');
}).on('click', "#multidata_view", function () {
    //
    // Services in list view
    //
    $("#services-result-listview").addClass('hidden');
    $("#services-result-multidata").removeClass('hidden');
});


function toggleArrows(element) {
    //
    //  Swap the direction of search engine
    //
    if (element.find(" .panel-collapse").hasClass("in")) {
        element.find("i").removeClass("fa-angle-double-down").addClass("fa-angle-double-up");
    }
    else {
        element.find("i").addClass("fa-angle-double-down").removeClass("fa-angle-double-up");
    }

}


function getCategories() {
    //
    // Load tree of categories and append it in search engine
    //
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
                    '<label for="category-' + data[root].id + '"> ' + data[root].title + '</label>',
                ].join('');

                
                for (var i in childs) {
                    var leafs = childs[i].children;
                    options += [
                        ((leafs .length> 0) ? startListInvisible : startList),
                        '<input type="checkbox" id="category-' + childs[i].id + '" name="category-' + childs[i].id + '" data-id="' + childs[i].id + '" data-name="category-' + childs[i].id + '"/>',
                        '<label for="category-' + childs[i].id + '"> ' + childs[i].title + '</label>',
                    ].join('');

                    
                    for (var j in leafs) {
                        options += [
                            startList,
                                '<input type="checkbox" id="category-' + leafs[j].id + '" name="category-' + leafs[j].id + '" data-id="' + leafs[j].id + '" data-name="category-' + leafs[j].id + '"/>',
                                    '<label for="category-' + leafs[j].id + '"> ' + leafs[j].title + '</label>',
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

function getResults(form, payload) {
    //
    // Retrieve the search results and append them
    //
    payload = parseRequest(payload);
    $.ajax({
        type: $(form).attr('method'),
        url: $(form).attr('action'),
        data: payload,
        beforeSend: function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (json) {
            var response = json.results;
            var multidata = "";
            var listview = "";
            if (!!response.length) {
                for (var i in response) {
                    //
                    // Load service image
                    //
                    var image = '';
                    if (response[i].image !== null) {
                        image += [
                            '<div style="height:130px; min-height:130px;">',
                                '<img class="img-responsive" style="border-bottom: 1px solid #ebebea; height: 130px !important" src="' + response[i].image_path + '" alt="' + gettext("Image relative to the service") + response[i].title + '">',
                            '</div>'
                        ].join('');
                    }
                    else {
                        image += '<div style="height:130px; min-height:130px; background-color: #ecebeb"></div>';
                    }
                    //
                    // Load provider logo
                    // 
                    var logo = "";
                    //if (response[i].logo !== null || response[i].logo !== undefined || response[i].logo !== "") {
                    //    logo += '<img src="/media/app/users/logos/' + response[i].logo + '" alt="' + response[i].logo + '" class="img-circle img-responsive" style="border: 1px solid whitesmoke;  min-height: 126px; max-height: 126px" />';
                    //}
                    //else {
                    logo += [
                        '<span class="fa-stack fa-1x" >',
                            '<i class="fa fa-circle fa-stack-2x" style="color: #d7d5d5;"></i>',
                            '<i class="fa fa-user fa-stack-1x" style="color: #ebebea"></i>',
                        '</span>'
                    ].join('');
                    //
                    // Service link
                    //
                    var link = "";
                    //var url = '{% url 'service_view_page' -1 %}'.replace(-1, response[i].id);
                    if (response[i].charging_model === 1) {
                        //link = '<a href="' + url + '" class="btn btn-success btn-xs">' + gettext('Access it!') + '</a>'; // href
                    }
                    else {
                        //link = '<a href="' + url + '" class="btn btn-success btn-xs">' + gettext('Get it!') + ' <i class="fa fa-shopping-cart"></i></a>'; // href
                    }
                    var price = (response[i].price === 0) ? gettext('FREE') : response[i].unit + " " + response[i].price;
                    //
                    // Load service in block view
                    //
                    multidata += appendServiceMultidata(response[i], image, logo, link, price);
                    $("#services-result-multidata").html(multidata);
                    //
                    // Load services in list view
                    //
                    listview += appendServiceListView(response[i], image, logo, link, price);
                    $("#services-result-listview").html(listview);
                    //
                    // Set the stars of any service based on its rating value
                    //
                    $(".service-banner").each(function () {
                        var rating = $(this).find("#srv-rating-" + $(this).attr("id").match(/\d+/)).find("span").first().text();
                        if (rating !== "None" && !(isNaN(rating))) {
                            for (var j = 1; j <= Math.ceil(rating) ; j++) {
                                $(this).find(".star-rating-" + j).removeClass("fa-star-o").addClass("fa-star");
                            }
                        }
                    });
                }
            }
            else {
                multidata += resultsNotFound();
                $("#services-result-multidata").html(multidata);
                listview = resultsNotFound();
                $("#services-result-listview").html(listview);
            }
        },
        error: function (error) { },
        complete: function (response) {
            //;
        },
    });

}

function parseRequest(search) {
    var request = "";
    if (search !== null) {
        request += "owners=" + ((search.owners.length > 0) ? search.owners.toString() + "&" : "null&");
        request += (search.categories.length > 0) ? "categories=" + search.categories.toString() + "&" : "";
        request += (search.types.length > 0) ? "types=" + search.types.toString() + "&" : "";
        request += (search.models.length > 0) ? "models=" + search.models.toString() + "&" : "";
        request += parseStringFilter("minPrice", search.minPrice);
        request += parseStringFilter("maxPrice", search.maxPrice);
        request += parseStringFilter("distance", search.distance);
        request += parseStringFilter("lat", search.lat);
        request += parseStringFilter("lon", search.lon);
        request += parseStringFilter("minQoS", search.minQoS);
        request += parseStringFilter("maxQoS", search.maxQoS);
        request += (search.sortby !== null) ? "sortby=" + search.sortby : "";
    }
    return request;
}

function parseStringFilter(name, value) {
    return (value !== null && value !== "") ? name + "=" + value + "&" : "";
}

function appendServiceMultidata(service, image, logo, link, price) {
    // return service item for block
    return [
        '<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4 on-mouseover service-banner" id="srv-' + service.id + '"  style="margin-bottom:25px !important">',
            '<div class="thumbnail" style="min-height:380px!important;">',
                image,
                '<div class="caption">',
                    '<div style="min-height:200px; max-height:200px">',
                        '<span class="fa-stack fa-3x img-responsive img-circle" style="margin-top:-55px">',
                            logo,
                        '</span>',
                        '<div class="row col-lg-12 col-sm-12 col-md-12 col-xs-12">',
                            '<a href="' + service.id + '" class="btn btn-link clearfix"><h4 class="text-center">' + service.title + '</h4></a>', // href
                        '</div>',
                        '<div class="row">',
                            '<div class="col-lg-12 col-sm-12 col-md-12 col-xs-12 text-justify">',
                                '<p class="clearfix">' + ((service.description.length > 0) ? service.description.substring(0, 130) + '...' : "") + '</p>',
                                link,
                            '</div>',
                        '</div>',
                    '</div>',
                    '<div style="min-height:50px; max-height:50px">',
                        '<div class="row">',
                            '<div class="col-sm-7 col-lg-7 col-md-7 col-xs-7" id="srv-rating-' + service.id + '" >',
                                '<span><strong>' + ((service.average_rating === null) ? gettext('None') : service.average_rating) + ' </strong></span> ',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-1"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-2"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-3"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-4"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-5"></span>',
                            '</div>',
                            '<div class="col-sm-5 col-lg-5 col-md-5 col-xs-5">',
                                '<strong class="pull-right">',
                                    price,
                                '</strong>',
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-8 col-lg-8 col-md-8 col-xs-8">',
                                '<em> ',
                                    '<span class="fa fa-comments-o fa-1x text-primary"></span> ',
                                    service.total_reviews + " " + ((service.total_reviews === 1) ? gettext('reviews') : gettext('review')),
                                '</em>',
                            '</div>',
                            '<div class="col-sm-4 col-lg-4 col-md-4 col-xs-4">',
                                    '<abbr title="' + ((service.type === "M") ? gettext('Machine-based service') : gettext('Human-based service')) + '"><span class="fa fa-laptop pull-right fa-2x" ></span></abbr>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>',
            '</div>',
        '</div>'
    ].join('');
}

function appendServiceListView(service, image, logo, link, price) {
    // return service item for list
    return [
        '<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12 on-mouseover service-banner" id="srv-' + service.id + '" style="margin-bottom: 3% ;min-height:inherit; margin-left:5px">',
            '<div class="row thumbnail">',
                '<div class="col-xs-12 col-sm-4 col-md-4 col-lg-4">',
                    image,
                '</div>',
                '<div class="caption col-xs-12 col-sm-8 col-md-8 col-lg-8">',
                    '<div class="row">',
                        '<div class="col-sm-3 col-md-3 col-lg-3">',
                            logo,
                        '</div>',
                        '<div class="col-sm-9 col-md-9 col-lg-9">',
                            //'<a href="{% url 'service_view_page' service.id %}" style="cursor: pointer!important"><h4>' + service.title + '</h4></a>',
                            '<div class="row">',
                                '<div class="col-lg-12 col-sm-12 col-md-12 col-xs-12">',
                                    '<p class="clearfix">' + ((service.description.length > 0) ? service.description.substring(0, 120) + '...' : "") + '</p>',
                                    link,
                                '</div>',
                            '</div>',
                        '<br>',
                        '<div class="row">',
                            '<div class="col-sm-7 col-lg-7 col-md-7 col-xs-7" id="srv-rating-' + service.id + '" >',
                                '<span><b>' + ((service.average_rating === null) ? gettext('None') : service.average_rating) + ' </b></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-1"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-2"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-3"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-4"></span>',
                                '<span class="fa fa-star-o star-colorize-yellow star-rating-5"></span>',
                            '</div>',
                            '<div class="col-sm-5 col-lg-5 col-md-5 col-xs-5">',
                                '<b class="pull-right">',
                                price,
                                '</b>',
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-8 col-lg-8 col-md-8 col-xs-8">',
                                '<em> ',
                                    '<span class="fa fa-comments-o fa-1x text-primary"></span> ',
                                    service.total_reviews + " " + ((service.total_reviews === 1) ? gettext('reviews') : gettext('review')),
                                '</em>',
                            '</div>',
                            '<div class="col-sm-4 col-lg-4 col-md-4 col-xs-4">',
                                '<abbr title="' + ((service.type === "M") ? gettext('Machine-based service') : gettext('Human-based service')) + '"><span class="fa fa-laptop pull-right fa-2x" ></span></abbr>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>',
            '</div>',
        '</div>',
    '</div>'

    ].join('');

}

function resultsNotFound() {
    return [
        '<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">',
            '<div class="alert alert-danger jumbotron">',
                '<h4 style="font-size: x-large" class="text-center">',
                    gettext("Results not found!"),
                '</h4>',
            '</div>',
        '</div>'
    ].join('');
}