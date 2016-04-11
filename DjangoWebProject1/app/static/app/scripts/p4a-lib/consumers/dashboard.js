
$(document).on('click', "#search-btn", function (event) {
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
        type: 'POST',
        url: "/services/search",
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
});

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
        }
    }
});

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
        type: 'POST',
        url: "/services/search",
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
        url: "/api/v1/categories/tree",
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