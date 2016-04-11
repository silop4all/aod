
var GoogleMap = GoogleMap || (function () {

    var defaultSelector = 'map';

    var latitude    = null;
    var longitude   = null;
    var coordinates = null;
    
    var settings = {
        strokeColor: 'red',
        strokeOpacity: 0.8,
        fillColor: '#AAAAAA',
        fillOpacity: 0.4,
        strokeWeight: 2,
        zoom: 11
    };


    var coverage = function coverage(radius) {
        // km
        return radius * 1000;
    }

    var details = function details(coordinates, title) {
        return [
            '<div>',
                '<strong>Service:</strong> ',
                title,
                '<br>',
                '<strong>Latitude:</strong> ',
                coordinates.latitude,
                '<br>',
                '<strong>Longitude:</strong> ',
                coordinates.longitude,
            '</div>'
        ].join('');
    }


    return {
        load: function (data, title, selector) {
            // data: latitude, longitude, radius
            coordinates = new google.maps.LatLng(data.latitude, data.longitude);

            defaultSelector = (selector != null) ? selector : defaultSelector;

            // Set options
            var options = {
                zoom: settings.zoom,
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

            var map = new google.maps.Map(document.getElementById(defaultSelector), options);
            var marker = new google.maps.Marker({
                position: coordinates,
                map: map,
                draggable: false
            });

            var area = new google.maps.Circle({
                strokeColor: settings.strokeColor,
                strokeOpacity:settings.strokeOpacity,
                strokeWeight: settings.strokeWeight,
                fillColor: settings.fillColor,
                fillOpacity: settings.fillOpacity,
                map: map,
                center: coordinates,
                radius: coverage(data.radius)
            });


            var infoWindow = new google.maps.InfoWindow({
                content: details(data, title)
            });

            // Handle user actions
            google.maps.event.addListener(marker, 'click', function (event) {
                infoWindow.open(map, marker);
            });
            // Set marker in center
            map.setCenter(marker.position);
            marker.setMap(map);
        }
    }
})();