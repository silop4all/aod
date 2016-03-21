/**
 * Function: HTML form (step-by-step) wizard
 * Author: panagiotis athanasoulis
 */


function Wizard() {
    // initiate empty list of cookies
    this.list = null;
    // initiate its name property
    this.name = null;
    // initiate its value property
    this.value = null;
}


/*
 * Prevent click event on disabled tabs. 
 * User can navigate in the wizard content using the previous/next buttons.
 */
function preventClickTab(tab) {
    if (tab.hasClass('disabled')) {
        return false;
    }
    return true;
}


/*
 * Proceed to the content of the next Tab altering the view of both current and new Tab.
 */
Wizard.prototype.nextStep = function () {
    // TODO
    var destination = $("#service-registration-wizard").find('li.active>a').attr("href");
    var newID = parseInt(destination.replace(/\D/g, '')) + parseInt(1);
    var next = "#step" + newID;
    if (newID <= 6) {

        var validation = true;
        if (validation) { // validate
            // change tab
            $('a[href="' + destination + '"]').parent().removeClass('active');
            $("#my-tab-content").find(destination).removeClass('active').removeClass('in');

            // load content of new tab
            $('a[href="' + next + '"]').parent().removeClass('disabled').addClass('active');
            $("#my-tab-content").find(next).addClass('active').addClass('in');
            $("#my-tab-content").find(next + '>div').animate("slow");
        }
    }



}

/*
 * Proceed to the content of the previous Tab altering the view of both current and new Tab.
 */
Wizard.prototype.previousStep = function () {
    // TODO
    var destination = $("#service-registration-wizard").find('li.active>a').attr("href");
    var newID = parseInt(destination.replace(/\D/g, '')) - parseInt(1);
    var previous = "#step" + newID;

    if (newID >= 1) {
        $('a[href="' + destination + '"]').parent().removeClass('active');
        $("#my-tab-content").find(destination).removeClass('active').removeClass('in');

        $('a[href="' + previous + '"]').parent().removeClass('disabled').addClass('active');
        $("#my-tab-content").find(previous).addClass('active').addClass('in');
    }
}