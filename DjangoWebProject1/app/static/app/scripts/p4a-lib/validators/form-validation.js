/*
 * Function: validate the service registration process
 * Author: panagiotis athanasoulis
 */

function ServiceRegistration(form) {
    // form
    this.form = form;
    // basic information
    this.title = '';
    this.description = '';
    this.cover = '';
    this.type = '';
    this.category = '';
    this.image = '';
    this.keywords = '';
    // charging
    this.chargingModel = '';
    this.price = '';
    this.currency = '';
    // usage
    this.requirements = '';
    this.link = '';
    this.usage = '';
    // constraints
    this.language = '';
    this.latitude = '';
    this.longitude = '';

    // constructor
    this.init();
}

ServiceRegistration.prototype.init = function () {
    // tab 1
    this.title = { control: $("#srv_title"), container: null, error: $("#srv_title_error"), status: false };
    this.description = { control: $("#srv_description"), container: $("#srv_description_node"), error: $("#srv_description_error"), status: false };
    this.cover = { control: $("#srv_cover_image"), container: $("#srv_cover_image_node"), error: $("#srv_cover_image_error"), status: false };
    this.type = { control: $("#srv_type"), container: $("#srv_type_node"), error: $("#srv_type_error"), status: false };
    this.category = { control: $("#srv_category"), container: $("#srv_category_node"), error: $("#srv_category_error"), status: false };
    this.image = { control: $("#srv_logo"), container: $("#load_logo"), error: $("#srv_logo_error"), status: false };
    this.keywords = { control: $("#srv_keyword_list"), container: null, error: $("#srv_keyword_list_error"), status: false };
    // tab 2
    this.model = { control: $("#srv_charging_model"), container: $("#srv_charging_model_node"), error: $("#srv_charging_model_error"), status: false };
    this.price = { control: $("#srv_price"), container: null, error: $("#srv_price_error"), status: false };
    this.currency = { control: $("#srv_currency"), container: $("#srv_currency_node"), error: $("#srv_currency_error"), status: false };
    // tab 3
    this.requirements = { control: $("#srv_requirements"), container: $("#srv_requirements_node"), error: $("#srv_requirements_error"), status: false };
    this.link = { control: $("#srv_link"), container: null, error: $("#srv_link_error"), status: false };
    this.usage = { control: $("#srv_usage"), container: $("#srv_usage_node"), error: $("#srv_usage_error"), status: false };
    // tab 4
    this.language = { control: $("#srv_language_constraint_y > i"), container: $("#srv_language"), error: $("#srv_language_error"), status: false };
    this.latitude = { control: $("#srv_latitude"), error: null, min: -90, max: 90, status: false }
    this.longitude = { control: $("#srv_latitude"), error: null, min: -180, max: 180, status: false }
    // tab 5
}

ServiceRegistration.prototype.basicInformationTab = function () {
    this.validateTitle();
    this.validateDescription();
    this.validateCoverImage();
    this.validateType();
    this.validateCategory();
    this.validateImage();
    this.validateKeywords();
    return (this.title.status && this.description.status && this.cover.status && this.type.status && this.category.status && this.image.status && this.keywords.status);
}
ServiceRegistration.prototype.validateTitle = function () {
    if (this.title.control.val().length == 0) {
        this.title.control.parent().addClass("has-error");
        //this.title.error.tooltip();
        this.title.status = false;
    }
    else {
        this.title.control.parent().removeClass("has-error");
        //this.title.error.tooltip('hide');
        this.title.status = true;
    }
}
ServiceRegistration.prototype.validateDescription = function () {
    if (this.description.control.val().length == 0) {
        this.description.control.parent().addClass("has-error");
        this.description.container.addClass("has-error");
        //this.description.error.tooltip('show');
        this.description.status = false;
    }
    else {
        this.description.control.parent().removeClass("has-error");
        this.description.container.removeClass("has-error");
        //this.description.error.tooltip('hide');
        this.description.status = true;
    }
}
ServiceRegistration.prototype.validateCoverImage = function () {
    if (this.cover.control.val() < 0 || this.cover.control.val() === undefined || this.cover.control.val() === null) {
        this.cover.control.parent().addClass('has-error');
        this.cover.container.addClass("error");
        //this.cover.error.tooltip('show');
        this.cover.status = false;
    }
    else {
        this.cover.control.parent().removeClass("has-error");
        this.cover.container.removeClass("error");
        //this.cover.error.tooltip('hide');
        this.cover.status = true;
    }
}
ServiceRegistration.prototype.validateType = function () {
    if (this.type.control.val() < 0 || this.type.control.val() === undefined || this.type.control.val() === null) {
        this.type.control.parent().addClass('has-error');
        this.type.container.addClass("error");
        //  this.type.error.tooltip('show');
        this.type.status = false;
    }
    else {
        this.type.control.parent().removeClass("has-error");
        this.type.container.removeClass("error");
        //this.type.error.tooltip('hide');
        this.type.status = true;
    }
}
ServiceRegistration.prototype.validateCategory = function () {
    if (this.category.control.val() < 0 || this.category.control.val() === undefined || this.category.control.val() === null) {
        this.category.control.parent().addClass('has-error');
        this.category.container.addClass("error");
        //  this.category.error.tooltip('show');
        this.category.status = false;
    }
    else {
        this.category.control.parent().removeClass("has-error");
        this.category.container.removeClass("error");
        //this.category.error.tooltip('hide');
        this.category.status = true;
    }
}
ServiceRegistration.prototype.validateImage= function () {
    if (this.image.control.val() === "" || this.image.control.val() === undefined || this.image.control.val() === null) {
        this.image.container.css("border-color", "#b94a48");
        this.image.status = false;
    }
    else {
        this.image.container.css("border-color", "");
        this.image.status = true;
    }
}
ServiceRegistration.prototype.validateKeywords = function () {
    if (this.keywords.control.val() === "" || this.keywords.control.val() === undefined || this.keywords.control.val() === null) {
        this.keywords.control.parent().addClass('has-error');
        //  this.keywords.error.tooltip('show');
        this.keywords.status = false;
    }
    else {
        this.keywords.control.parent().removeClass("has-error");
        //this.keywords.error.tooltip('hide');
        this.keywords.status = true;
    }
}

ServiceRegistration.prototype.chargingTab = function () {
    this.validateModel();
    this.validatePrice();
    this.validateCurrency();
    return (this.model.status && this.price.status && this.currency.status);
}
ServiceRegistration.prototype.validateModel = function () {
    if (this.model.control.val() < 0 || this.model.control.val() === undefined || this.model.control.val() === null) {
        this.model.control.parent().addClass('has-error');
        this.model.container.addClass("error");
        // this.model.error.tooltip('show');
        this.model.status = false;
    }
    else {
        this.model.control.parent().removeClass("has-error");
        this.model.container.removeClass("error");
        //this.model.error.tooltip('hide');
        this.model.status = true;
    }
}
ServiceRegistration.prototype.validatePrice = function () {

    if (this.model.control.find("option :selected") === 1 || this.model.control.find("option :selected").text() == "None charge") {
       this.price.status = false;
    }
    else {
        if (this.price.control.val() < 0.0 || isNaN(this.price.control.val()) || this.price.control.val().length == 0) {
            this.price.control.parent().addClass('has-error');
            // this.price.error.tooltip('show');
            this.price.status = false;
        }
        else {
            this.price.control.parent().removeClass("has-error");
            //this.price.error.tooltip('hide');
            this.price.status = true;
        }
    }
}
ServiceRegistration.prototype.validateCurrency = function () {
    if (this.currency.control.val() < 0 || this.currency.control.val() === undefined || this.currency.control.val() === null) {
        this.currency.control.parent().addClass('has-error');
        this.currency.container.addClass("error");
        // this.currency.error.tooltip('show');
        this.currency.status = false;
    }
    else {
        this.currency.control.parent().removeClass("has-error");
        this.currency.container.removeClass("error");
        //this.currency.error.tooltip('hide');
        this.currency.status = true;
    }
}

ServiceRegistration.prototype.usageTab = function () {
    this.validateRequirements();
    this.validateLink();
    this.validateUsage();
    return (this.requirements.status && this.link.status && this.usage.status);
}
ServiceRegistration.prototype.validateRequirements = function () {
    if (this.requirements.control.val().length == 0) {
        this.requirements.control.parent().addClass("has-error");
        this.requirements.container.addClass("has-error");
        // this.requirements.error.tooltip('show');
        this.requirements.status = false;
    }
    else {
        this.requirements.control.parent().removeClass("has-error");
        this.requirements.container.removeClass("has-error");
        //this.requirements.error.tooltip('hide');
        this.requirements.status = true;
    }
}
ServiceRegistration.prototype.validateLink = function () {
    this.link.status = true;
}
ServiceRegistration.prototype.validateUsage = function () {
    if (this.usage.control.val().length == 0) {
        this.usage.control.parent().addClass("has-error");
        this.usage.container.addClass("has-error");
        //this.usage.error.tooltip('show');
        this.usage.status = false;
    }
    else {
        this.usage.control.parent().removeClass("has-error");
        this.usage.container.removeClass("has-error");
        //this.usage.error.tooltip('hide');
        this.usage.status = true;
    }
}

ServiceRegistration.prototype.constraintsTab = function () {
    this.validateLatitude();
    this.validateLongitude();
    this.validateLanguageList();
    return (this.latitude.status && this.longitude.status && this.language.status);
}
ServiceRegistration.prototype.validateLanguageList = function () {
    if (this.language.control.hasClass('fa-check-square-o')) {
        if (this.language.container.val() === "" || this.language.container.val() === null) {
            this.language.container.parent().addClass('has-error');
            this.language.container.parent().addClass('error');
            // error info
            this.language.status = false;
            return;
        }
    }
    this.language.container.parent().removeClass('has-error');
    this.language.container.parent().removeClass('error');
    // info
    this.language.status = true;
}
ServiceRegistration.prototype.validateLatitude = function () {
    if ( (this.latitude.control.val() < this.latitude.min || this.latitude.control.val() > this.latitude.max) || isNaN(this.latitude.control.val()) || this.latitude.control.val() === "" ) {
        this.latitude.control.parent().parent().addClass("has-error");
        // this.latitude.error.tooltip('show');
        this.latitude.status = false;
    }
    else {
        this.latitude.control.parent().parent().removeClass("has-error");
        // this.latitude.error.tooltip('hide');
        this.latitude.status = true;
    }
}
ServiceRegistration.prototype.validateLongitude = function () {
    if (this.longitude.control.val().length != 0 && (this.longitude.control.val() < this.longitude.min || this.longitude.control.val() > this.longitude.max) || isNaN(this.longitude.control.val())) {
        this.longitude.control.parent().addClass("has-error");
        // this.longitude.error.tooltip('show');
        this.longitude.status = false;
    }
    else {
        this.longitude.control.parent().removeClass("has-error");
        // this.longitude.error.tooltip('hide');
        this.longitude.status = true;
    }
}

ServiceRegistration.prototype.supportTab = function () {
    return true;
}

ServiceRegistration.prototype.confirmTab = function () {
    return true;
}