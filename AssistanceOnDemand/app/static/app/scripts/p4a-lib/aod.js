/**
 * Module:      JS lib
 * Dependency:  jQuery
 */



var AoD = AoD || (function () {
    //
    // local variables
    //
    var currentForm = null;
    var currentValidator = null;
    var errorClass = "aod-invalid-field";
    var eSettings = {
        validatorClass: errorClass,
        highlightClass: 'has-error',
        highlightTextClass: "highlight-error-message",
    }
    //
    // custom validation rules
    //
    $.validator.addMethod("notEqualWithSelector", function (value, element, param) {
        return this.optional(element) || (value !== $(param).val());
    });
    $.validator.addMethod("notEqualWithStr", function (value, element, param) {
        return param != value;
    });
    $.validator.addMethod("notNegativeNumber", function (value, element, param) {
        return value >= 0.0;
    });
    $.validator.addMethod("existNumberConstraint", function (value, element, param) {
        // if location constraint exists, check if field has valid value
        if (!!$(param).find($(".fa-check-square-o")).length) {
            hasValue = !(isNaN($(element).val()) || $(element).val() === "");
            return hasValue;
        }
        return true;
    });
    $.validator.addMethod("existStringConstraint", function (value, element, param) {
        // if language constraint exists, check if exist selected value(s) in list
        if (!!$(param).find($(".fa-check-square-o")).length) {
            hasValue = !($(element).val() === "" || $(element).val() === null);
            return hasValue;
        }
        return true;
    });
    //$.validator.addMethod("serviceImage", function (value, element, param) {
    //    if ($("#thumbnail").attr("src") !== param) {
    //        return true;
    //    }
    //    return false;
    //});

    
    
    //
    // Serialize form data
    //
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (this.value !== "") {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            }
        });
        return o;
    };

    $.fn.serializeObjectAll = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

    $.fn.serializeList = function () {
        var o = [];
        var a = this.serializeArray();
        $.each(a, function () {
            if (!isNaN(this.name)) {
                o.push(parseInt(this.name));
            }
        })
        return o;
    };



    // global scope
    return {
        //
        // validate Service Forms
        //
        validateBasicServiceForm: function (currentForm) {
            //
            // validate Basic Tab
            //
            preRegValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    title: {
                        required: true,
                        maxlength: 128
                    },
                    description: {
                        required: true,
                    },
                    type: {
                        required: true,
                        notEqualWithStr: "-1"
                    },
                    categories: {
                        required: true,
                        notEqualWithStr: ""
                    },
                    //thumbnail: {
                    //    required: true,
                    //    serviceImage: "#"
                    //},
                    version: {
                        required: false,
                        maxlength: 10
                    },
                    license: {
                        required: false,
                        maxlength: 30
                    },
                    keywords: {
                        required: true
                    }
                },
                messages: {
                    title: {
                        required: gettext("Please enter the title of your service"),
                    },
                    description: {
                        required: gettext("Please describe the service you offer"),
                    },
                    type: {
                        required: gettext("Please clarify the type of your service"),
                        notEqualWithStr: gettext("Please select the type of the service")
                    },
                    categories: {
                        required: gettext("Please choose the categories that your service belongs to"),
                        notEqualWithStr: gettext("Please choose at least one category"),
                    },
                    //image: {
                    //    required: gettext("Please upload an image for you service"),
                    //    accept: gettext("Please upload an image. This file is not supported")
                    //},
                    keywords: {
                        required: gettext("Please enter at least one keyword for your service"),
                    }
                },
                errorPlacement: function (error, element) {
                    if (element.attr("name") === "type") {
                        $("#type_node").addClass('error');
                        error.insertAfter(element.parent());
                        error.addClass(eSettings.highlightTextClass).addClass("row col-sm-offset-3 col-md-offset-3 col-lg-offset-3");
                    }
                    else if (element.attr("name") === "categories") {
                        $("#category_node").addClass('error');
                        error.insertAfter(element.parent());
                        error.addClass(eSettings.highlightTextClass).addClass("row col-sm-offset-3 col-md-offset-3 col-lg-offset-3  col-sm-8 col-md-8 col-lg-8");
                    } else {
                        error.insertAfter(element);
                        error.addClass(eSettings.highlightTextClass);
                    }
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    if (error.parent().find($("#type")).length > 0) {
                        $("#type_node").removeClass('error');
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                    }
                    else if (error.parent().find($("#categories")).length > 0) {
                        $("#category_node").removeClass('error');
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                    }
                    else {
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                        error.parent().find($("div")).remove();
                    }
                }
            });
            $(currentForm).validate().settings.ignore = "";
            console.log($(currentForm).serializeObject());
        },
        validatePaymentServiceForm: function (form) {
            //
            // validate Payment Tab
            //
            preRegValidator = $(form).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    charging_policy: {
                        required: true,
                        notEqualWithStr: ""
                    },
                    price: {
                        required: true,
                        number: true,
                        notNegativeNumber: true
                    },
                    unit: {
                        required: true,
                        notEqualWithStr: ""
                    }
                },
                messages: {
                    charging_policy: {
                        required: gettext("Please declare the charing policy"),
                        notEqualWithStr: gettext("Please choose one policy"),
                    },
                    price: {
                        required: gettext("Please set the price of the service"),
                        number: gettext("Please enter only digits"),
                        notNegativeNumber: gettext("Please enter a non negative number")
                    },
                    unit: {
                        required: gettext("Please set the unit/currency of the service"),
                    }
                },
                errorPlacement: function (error, element) {
                    if (element.attr("name") === "charging_policy") {
                        $("#charging_policy_node").addClass('error');
                        error.insertAfter(element.parent());
                        error.addClass(eSettings.highlightTextClass).addClass("row col-sm-offset-3 col-md-offset-3 col-lg-offset-3  col-sm-8 col-md-8 col-lg-8");
                    }
                    else if (element.attr("name") === "unit") {
                        $("#unit_node").addClass('error');
                        error.insertAfter(element.parent());
                        error.addClass(eSettings.highlightTextClass).addClass("row col-sm-offset-3 col-md-offset-3 col-lg-offset-3  col-sm-8 col-md-8 col-lg-8");
                    } else {
                        error.insertAfter(element);
                        error.addClass(eSettings.highlightTextClass);
                    }
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    if (error.parent().find($("#charging_policy")).length > 0) {
                        $("#charging_policy_node").removeClass('error');
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                    }
                    else if (error.parent().find($("#unit")).length > 0) {
                        $("#unit_node").removeClass('error');
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                    }
                    else {
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                        error.parent().find($("div")).remove();
                    }
                }
            });
            $(form).validate().settings.ignore = "";
            console.log($(form).serializeObject());
        },
        validateUsageServiceForm: function(form){
            //
            // validate Usage Tab
            //
            //preRegValidator = $(form).validate({
            //    errorClass: errorClass,
            //    errorElement: "div",
            //    rules: {
            //    },
            //    messages: {
            //    },
            //    errorPlacement: function (error, element) {

            //    },
            //    success: function (error) {
            //    }
            //});
            //$(form).validate().settings.ignore = "";
            console.log($(form).serializeObject());
        },
        validateConstraintsServiceForm: function(form){
            //
            // validate Constraints Tab
            //
            preRegValidator = $(form).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    languages: {
                        required: false,
                        existStringConstraint: "#language_constraint_yes"
                    },
                    latitude: {
                        required: false,
                        number: true,
                        min: -90,
                        max: 90,
                        existNumberConstraint: "#location_constraint_yes"
                    },
                    longitude: {
                        required: false,
                        number: true,
                        min: -180,
                        max: 180,
                        existNumberConstraint: "#location_constraint_yes"
                    },
                    coverage: {
                        required: false,
                        number: true,
                        min: 0,
                        existNumberConstraint: "#location_constraint_yes"
                    }
                },
                messages: {
                    languages: {
                        required: false,
                        existStringConstraint: gettext("Please select from the list the languages in which the service is supported")
                    },
                    latitude: {
                        number: gettext("Please enter a numerous value in range ") + "[-90, 90]",
                        existNumberConstraint: gettext("Please enter a numerous value in range ") + "[-90, 90]",
                    },
                    longitude: {
                        number: gettext("Please enter a numerous value in range ") + "[-180, 180]",
                        existNumberConstraint: gettext("Please enter a numerous value in range ") + "[-180, 180]",
                    },
                    coverage: {
                        number: gettext("Please enter a non negative numerous value"),
                        existNumberConstraint: gettext("Please enter a non negative numerous value"),
                    }
                },
                errorPlacement: function (error, element) {
                    if (element.attr("name") === "languages") {
                        $("#language_node").addClass('error');
                        error.insertAfter(element.parent());
                        error.addClass(eSettings.highlightTextClass).addClass("row col-sm-offset-3 col-md-offset-3 col-lg-offset-3 col-sm-8 col-md-8 col-lg-8");
                    }
                    else {
                        error.insertAfter(element);
                        error.addClass(eSettings.highlightTextClass);
                        element.parent().addClass(eSettings.highlightClass);
                    }
                    //element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    if (error.parent().find($("#languages")).length > 0) {
                        $("#language_node").removeClass('error');
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                    }
                    else {
                        error.parent().removeClass(eSettings.highlightClass);
                        error.removeClass(errorClass);
                        error.parent().find($("div")).remove();
                    }
                }
            });
            $(form).validate().settings.ignore = "";
            console.log($(form).serializeObject());
        },
        validateSupportServiceForm: function(form){
            //
            // validate Support Tab
            //
            //preRegValidator = $(form).validate({
            //    errorClass: errorClass,
            //    errorElement: "div",
            //    rules: {
            //    },
            //    messages: {
            //    },
            //    errorPlacement: function (error, element) {

            //    },
            //    success: function (error) {
            //    }
            //});
            //$(form).validate().settings.ignore = "";
            console.log($(form).serializeObject());
        },
        validateConfirmServiceForm: function(form) {
            //
            // validate Confirm Tab
            //
            preRegValidator = $(form).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    is_visible: {
                        required: true
                    },
                    terms: {
                        required: true
                    }
                },
                messages: {
                    is_visible: {
                        required: gettext('Clarify if you want to publish your service on users')
                    },
                    terms: {
                        required: gettext("Please read the <strong>Terms of usage</strong> and then check the box if you agree with it"),
                    }
                },
                errorPlacement: function (error, element) {
                    //if (element.attr('id') === "terms") {
                    if (element.attr('type') === "checkbox") {
                        error.insertAfter($(form).find("#terms_div"));
                    }
                    else if (element.attr('type') === "radio")  {
                        error.insertAfter($("#is_visible_div"));
                    }
                    error.addClass(eSettings.highlightTextClass);
                    element.parent().addClass(eSettings.highlightClass);
                    
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    var payload = {};
                    var files = new FormData($("#BasicServiceForm")[0]);
                    var SnIntegration = null;
                    var SnUrl = null;
                    var mediaUrl = null;
                    var auth = null;
                    var succesUrl = null;
                    if ($("#register-btn").length) {
                        succesUrl = $("#register-btn").data('successUrl');
                    }
                    else {
                        succesUrl = $("#update-btn").data('successUrl');
                    }
                    //
                    // compose payload
                    //
                    $.extend(payload, $("#BasicServiceForm").serializeObject());
                    $.extend(payload, $("#PaymentServiceForm").serializeObject());
                    $.extend(payload, $("#UsageServiceForm").serializeObject());
                    $.extend(payload, $("#ConstraintsServiceForm").serializeObject());
                    $.extend(payload, $("#SupportServiceForm").serializeObject());
                    $.extend(payload, $("#ConfirmServiceForm").serializeObjectAll());
                    payload["is_public"] = ($("#is_public").find("a.btn-primary").attr("id") === 'availability_pb') ? 1 : 0;
                    payload["language_constraint"] = ($("#language_constraint").find("a.btn-primary").attr("id") === 'language_constraint_yes') ? 1 : 0;
                    payload["location_constraint"] = ($("#location_constraint").find("a.btn-primary").attr("id") == 'location_constraint_yes') ? 1 : 0;
                    if (typeof (payload["categories"]) !== "object")
                        payload["categories"] = [payload["categories"]];
                    if ("languages" in payload && typeof (payload["languages"]) !== "object")
                        payload["languages"] = [payload["languages"]];
                    //
                    // register service
                    // 
                    var loading = new AjaxView($("#service-registration-wizard"));
                    loading.show();
                    $.ajax({
                        type: $(form).attr('method'),
                        url: $(form).attr('action'),
                        dataType: "json",
                        beforeSend: function (xhr, settings) {
                            $.ajaxSettings.beforeSend(xhr, settings);
                        },
                        contentType: 'application/json',
                        data: JSON.stringify(payload),
                        success: function (response) {
                            SnIntegration = response.sn_integration;
                            SnUrl = response.sn_link;
                            mediaUrl = response.media_url;
                            auth = response.auth_basic;
                            //
                            // Service media
                            //
                            $.ajax({
                                type: 'PUT',
                                url: mediaUrl,
                                data: files,
                                cache: false,
                                contentType: false,
                                processData: false,
                                success: function (response) {
                                    console.info(gettext("Image has been uploaded"));
                                },
                                error: function (error) {
                                    console.error(gettext("Error in image uploading"));
                                },
                                complete: function () {
                                    //
                                    // Social network
                                    //
                                    if (SnIntegration === true) {
                                        $.ajax({
                                            type: 'GET',
                                            url: SnUrl,
                                            headers: {
                                                "Authorization": "Basic " + auth
                                            },
                                            success: function (snResponse) {
                                                console.info(snResponse);
                                                if (snResponse.result !== "OK") {
                                                    console.error(snResponse);
                                                }
                                            },
                                            error: function (error) {
                                                console.error(error);
                                            },
                                            complete: function () {
                                            }
                                        });
                                    }
                                    loading.hide();
                                    location.href = succesUrl;
                                }
                            });
                        },
                        error: function (response) {
                            console.log(response);
                            var messages = JSON.parse(response.responseText).reason[0];
                            var fieldError = Object.keys(JSON.parse(response.responseText).reason[0])
                            loading.hide();
                            swal({
                                title: gettext("Error in service registration process"),
                                text: (fieldError !== undefined) ? messages[fieldError] : gettext("Try again. An error has occurred!"),
                                type: "error",
                                confirmButtonText: gettext("Continue"),
                                confirmButtonColor: "#3a87ad",
                                animation: "slide-from-top"
                            });
                        },
                        complete: function () {
                            loading.hide();
                        }
                    });
                }
            });
        },
        //
        // contactUsForm
        //
        contactUsForm: function (completeUrl) {
            currentForm = '#ContactUsForm';

            preRegValidator = $(currentForm).validate({
                errorClass: errorClass,
                errorElement: "span",
                rules: {
                    user: {
                        required: true,
                    },
                    email: {
                        required: true,
                        email: true,
                    },
                    subject: {
                        required: true,
                    },
                    message: {
                        required: true
                    }
                },
                messages: {
                    user: {
                        required: gettext("Please enter your name and lastname"),
                    },
                    mail: {
                        required: gettext("Please enter your email address"),
                        email: gettext("Your email address must be in the format of name@domain.org")
                    },
                    subject: {
                        required: gettext("Please clarify the subject of the message"),
                    },
                    message: {
                        required: gettext("Please enter the message"),
                    },
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.addClass("highlight-error-message");
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("span")).remove();
                },
                submitHandler: function (form) {
                    $.ajax({
                        url: $(form).attr('action'),
                        type: $(form).attr('method'),
                        dataType: "json",
                        contentType: 'application/json',
                        data: JSON.stringify($(form).serializeObject()),
                        success: function (response) {
                            console.info(gettext("OK"));
                        },
                        error: function (response) {
                            console.info(gettext("Error"));
                        },
                        complete: function () {
                            swal({
                                html: false,
                                title: gettext("Message progress"),
                                text: gettext('Your message has been submitted'),
                                type: "info",
                                confirmButtonText: gettext("Continue"),
                                confirmButtonColor: "#d9534f"
                            },
                            function (isConfirm) {
                                if (isConfirm) {
                                    location.href = completeUrl;
                                }
                            });
                            return;
                        }
                    });
                }
            });
        },
    }

})();