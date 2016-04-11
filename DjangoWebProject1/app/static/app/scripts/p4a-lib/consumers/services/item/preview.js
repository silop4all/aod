
//$(document).ready(function () {
//    // Preview tab: slider
//    loadImageSlider();
    
//    // Statistics tab
//    $('#table').bootstrapTable({
//        //data: loadStatistics()
//        data: data
//    });
//    $("#download_sw").click(function (event) {
//        event.preventDefault();
//        window.location.href = $(this).data().link;
//    });
//});


//$(document).on('', '', function () {

//    /api/v1/services/2/support


//});

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


function loadStatistics() {
    // stats
    var data = [
        {
            'user': 'Nick Tatopoulos',
            'purchased_date': '2015-04-12 12:34:34',
            'cost': 0.00,
            'payment_status': 'Pending',
            'payment_date': 'N/A'
        },
        {
            'user': 'Takis Arakans',
            'purchased_date': '2015-04-09 02:54:12',
            'cost': 0.00,
            'payment_status': 'Completed',
            'payment_date': 'N/A'
        }
    ]
    return data;
}

