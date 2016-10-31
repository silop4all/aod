/**
 * Function: Display a icon while any AJAX call is executing. It uses the "fa awesome" library of icons.
 * Dependency: jquery.blockUI.js, fa awesome lib/link
 * Author: panagiotis athanasoulis
 */

// Define a class like this
function AjaxView(element) {
    // set element
    this.element = element;
    // set offsets
    this.padding = 0;
    this.margin = 0;
    // set bounds
    this.width = '30%';
    this.top = '40%';
    this.left = '35%';
    // text align
    this.textAlign = 'center';
    // cursor view
    this.cursor = 'wait';
    // set colors etc
    this.backgroundColor = "transparent!important";
    this.border = '0px solid #fff !important';
    this.color = "forestgreen!important";
    this.opacity = 0.7;
    this.position = "absolute";

    // settings
    this.settings = {
        padding: this.padding,
        margin: this.margin,
        width: this.width,
        top: this.top,
        left: this.left,
        textAlign: this.textAlign,
        cursor: this.cursor,
        backgroundColor: this.backgroundColor,
        border: this.border,
        color: this.color,
        opacity: this.opacity,
        position: this.position
    }

    // message that is displayed
    this.message = "<i class='fa fa-spinner fa-pulse fa-5x test-success'></i>";

    // fade in/out
    this.fadeIn = 0;
    this.fadeOut = 0;
}

AjaxView.prototype.show = function () {
    // block a section or area 
    this.element.block({
        fadeIn: this.fadeIn,
        fadeOut: this.fadeOut,
        css: this.settings,
        message: this.message
    });
}

AjaxView.prototype.hide = function () {
    // terminate block after ajax termination
    this.element.unblock({});
}

AjaxView.prototype.loadall = function () {
    // load whole document
    $.blockUI.defaults.css = this.settings;
    $.blockUI.defaults.fadeIn = this.fadeIn;
    $.blockUI.defaults.fadeOut = this.fadeOut;
    $.blockUI({ message: this.message });
}