/**
 * Function: Instantiate a Cookie object. Get the value of a specific cookie name.
 *
 * Author: panagiotis athanasoulis
 */


function Cookies() {
    // initiate empty list of cookies
    this.list = null;
    // initiate its name property
    this.name = null;
    // initiate its value property
    this.value = null;
}


Cookies.prototype.getValue = function (name) {
    // set name
    this.name = name;

    // search
    if (document.cookie && document.cookie != '') {
        // set a list of cookies
        this.list = document.cookie.split(';');

        for (var i = 0; i < this.list.length; i++) {
            var cookie = $.trim(this.list[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                this.value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    // get the cookie value
    return this.value;
}


Cookies.prototype.setValue = function (name, value, expiration) {
    this.name   = name;
    this.value = value;
    this.expiration = expiration;

    var CookieDate = new Date;
    CookieDate.setFullYear(CookieDate.getFullYear() + expiration);
    this.value = escape(this.value) + ((expiration == null) ? "" : "; expires=" + CookieDate.toGMTString());
    document.cookie = this.name + "=" + this.value;
}
