/**
 * Function: Swap a set of properties (color, nested icons etc) among two buttons. It uses the "fa awesome" library of icons.
 *
 * Author: panagiotis athanasoulis
 */

// Define a class like this
function Swap2Buttons(btnA, btnB) {
    // set the ID attributes of each button
    this.btnA = btnA;   // set the id element of 1st button
    this.btnB = btnB;   // set the id element of 2nd button

    this.childNodeA = "i";
    this.childNodeB = "i";

    // set the classes to generate the nested icons 
    this.iconA = "fa-check-square-o";
    this.iconB = "fa-square-o";
    this.tempIconA = null;
    this.tempIconB = null;
    
    // colors
    this.colorA = "btn-primary";
    this.colorB = "btn-default";
    this.tempColorA = null;
    this.tempColorB = null;

    // debug state
    this.debug = false;
}

Swap2Buttons.prototype.setDebug = function (state) {
    // Override the predefined debug state
    this.debug = state;
    console.log("Debug state: "+ this.debug);
}

Swap2Buttons.prototype.setChildNodes = function (chNodeA, chNodeB) {
    // 
    this.childNodeA = chNodeA;
    this.childNodeB = chNodeB;

    if (this.debug) { 
        console.log("Child node of btn A:" + this.childNodeA); 
        console.log("Child node of btn B:" + this.childNodeB);
    }
}

Swap2Buttons.prototype.setIcons = function (iconClassA, iconClassB) {
    // override the predefined values of properties
    this.iconA = iconClassA;
    this.iconB = iconClassB;

    if (this.debug) {
        console.log("Icon of btn A:" + this.iconA);
        console.log("Icon of btn B:" + this.iconB);
    }
}

Swap2Buttons.prototype.setColors = function (colorClassA, colorClassB) {
    // override the predefined color class of properties
    this.colorA = colorClassA;
    this.colorB = colorClassB;

    if (this.debug) {
        console.log("Color of btn A:" + this.iconA);
        console.log("Color of btn B:" + this.iconB);
    }
}


Swap2Buttons.prototype.click = function (currentBtn) {
    // Handle click events
    if (this.btnA.attr("id") == currentBtn.attr("id")) {
        this.initiate();
    }
    else {
        this.swap();
    }
}

Swap2Buttons.prototype.initiate = function () {
    // Swap buttons properties
    this.btnA.find(this.childNodeA).removeClass(this.iconB).addClass(this.iconA);
    this.btnA.removeClass(this.colorB).addClass(this.colorA);
    this.btnB.find(this.childNodeB).removeClass(this.iconA).addClass(this.iconB);
    this.btnB.removeClass(this.colorA).addClass(this.colorB);

    if (this.debug) {
        console.log("Initiate properties of buttons");
        console.log(this.btnA);
        console.log(this.btnB);
    }
}

Swap2Buttons.prototype.swap = function () {
    // Swap buttons properties
    this.btnB.find(this.childNodeB).removeClass(this.iconB).addClass(this.iconA);
    this.btnB.removeClass(this.colorB).addClass(this.colorA);
    this.btnA.find(this.childNodeA).removeClass(this.iconA).addClass(this.iconB);
    this.btnA.removeClass(this.colorA).addClass(this.colorB);

    if (this.debug) {
        console.log("Swap properties of buttons");
        console.log(this.btnA);
        console.log(this.btnB);
    }
}

Swap2Buttons.prototype.log = function () {
    // Logs
    console.log("First button:" + this.btnA);
    console.log("Second button:" + this.btnB);
}
