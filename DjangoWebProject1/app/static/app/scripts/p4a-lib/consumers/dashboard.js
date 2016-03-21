
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
        alert("The price values must be non negative numbers!");
        return;
    }
    if (search.minPrice > search.maxPrice) {
        alert("The price values are invalid!");
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
        alert("The minimum value of QoS is out of range [0,5]");
        return;
    }
    if (search.maxQoS < 0 || search.maxQoS > 5) {
        alert("The maximum value of QoS is out of range [0,5]");
        return;
    }
    if (search.minQoS > search.maxQoS) {
        alert("The QoS values is invalid");
        return;
    }


    // distance threshold
    search.distance = $("div#location-id").find('input').val();
    if (search.distance < 0) {
        alert("The distance value must be a non negative number.");
        return;
    }
    // inform user for location tracking
    if (search.distance !== ""){
        var retVal = confirm("The AoD platform wants your permission to track your location. Do you agree with this action?");
        if (retVal == false) {
            alert("The service searching was aborted.");
            return;
        }
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
        alert("The price values must be non negative numbers!");
        return;
    }
    if (search.minPrice > search.maxPrice) {
        alert("The price values are invalid!");
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
        alert("The minimum value of QoS is out of range [0,5]");
        return;
    }
    if (search.maxQoS < 0 || search.maxQoS > 5) {
        alert("The maximum value of QoS is out of range [0,5]");
        return;
    }
    if (search.minQoS > search.maxQoS) {
        alert("The QoS values is invalid");
        return;
    }


    // distance threshold
    search.distance = $("div#location-id").find('input').val();
    if (search.distance < 0) {
        alert("The distance value must be a non negative number.");
        return;
    }
    // inform user for location tracking
    if (search.distance !== "") {
        var retVal = confirm("The AoD platform wants your permission to track your location. Do you agree with this action?");
        if (retVal == false) {
            alert("The service searching was aborted.");
            return;
        }
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