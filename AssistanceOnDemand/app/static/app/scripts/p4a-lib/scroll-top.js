
$(document).ready(function () {

    //Check to see if the window is top if not then display button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            //$('#top-link-block').fadeIn('slow');
            $('#top-link-block').removeClass('hidden');
        } else {
            //$('#top-link-block').fadeOut();
            $('#top-link-block').addClass('hidden');
        }
    });

    //Click event to scroll to top
    $('.scrollToTop').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 800);
        return false;
    });

    goTop();

});


// Go to the top
function goTop() {
    $('html,body').animate({ scrollTop: 0 }, 800);
    return false;
}