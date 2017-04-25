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

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", new Cookies().getValue('csrftoken'));
            }
        }
    });

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
                                type: 'POST',
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
        // register new technical material for a service
        //
        registerServiceTechnicalMaterial: function (form, successURL) {
            preRegValidator = $(form).validate({
                errorClass: errorClass,
                errorElement: "div",
                rules: {
                    title: {
                        required: true,
                        maxlength: 128
                    },
                },
                messages: {
                    title: {
                        required: gettext("Please enter the title of the material"),
                    },
                },
                errorPlacement: function (error, element) {
                    error.insertAfter(element);
                    error.addClass(eSettings.highlightTextClass);
                    element.parent().addClass(eSettings.highlightClass);
                },
                success: function (error) {
                    error.parent().removeClass(eSettings.highlightClass);
                    error.removeClass(errorClass);
                    error.parent().find($("div")).remove();
                },
                submitHandler: function (form) {

                    $.when(
                        $.ajax({
                            url: $(form).attr('action'),
                            type: $(form).attr('method'),
                            dataType: "json",
                            beforeSend: function (xhr, settings) {
                                $.ajaxSettings.beforeSend(xhr, settings);
                            },
                            contentType: 'application/json',
                            data: JSON.stringify($(form).serializeObject()),
                            success: function (response) {
                                console.log(response);
                            },
                            error: function (response) {
                                console.info("error");
                            },
                            complete: function (res) {
                                console.info("Completed");
                            }
                        })
                    ).done(function (response) {
                        if (!!response.uploadFile === true) {
                            //
                            // Upload material
                            //
                            var fdata = new FormData();
                            var file = $("#material").get(0).files[0];
                            fdata.append("material", file);

                            if (fdata.has("material") === true) {
                                $.ajax({
                                    type: 'POST',
                                    url: response.uploadMediaURL,
                                    data: fdata,
                                    cache: false,
                                    enctype: "multipart/form-data",
                                    contentType: false,
                                    processData: false,
                                    success: function (fileResponse) {
                                        console.info(gettext("Material has been uploaded"));
                                    },
                                    error: function (error) {
                                        console.log(gettext("Material did not upload to server"));
                                    },
                                    complete: function () {
                                        location.reload();
                                    }
                                });
                            }
                            else {
                                location.reload();
                            }
                        }
                        else {
                            location.reload();
                        }
                    });
                }
            });
        },
        //
        // retrieve the technical material for a service
        //
        retrieveServiceTechnicalMaterial: function (url, media_path, baseURL) {
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                contentType: 'application/json',
                success: function (response) {
                    //
                    // Preview material on the right side of page
                    //
                    var preview = "";
                    var resourceUrl = response.path;
                    
                    if (response.extension.toLowerCase() === "pdf") {
                        preview = [
                            '<object data="' + resourceUrl + '" type="application/pdf" height="380" width="100%">',
                                '<embed src="' +  resourceUrl + '" type="application/pdf" />',
                            '</object>'
                        ].join('');

                    }
                    else if (response.extension.toLowerCase() === "mp4") {
                        preview = [
                            '<div class="embed-responsive embed-responsive-16by9 videoUiWrapper">',
                                '<span class="padding-bottom-10"></span>',
                                '<video style="width:100%" controls  title="" class="embed-responsive-item">',
                                    '<source src="' + resourceUrl + '" type="video/mp4">',
                                    gettext('Your browser does not support the video tag.'),
                                '</video>',
                            '</div>'
                        ].join('');
                    }
                    else {
                        if (response.technical_support.id === 1) {
                            // youtube embed
                            preview = [
                                '<div class="embed-responsive embed-responsive-4by3">',
                                    '<iframe title="YouTube video player" class="youtube-player embed-responsive-item" type="text/html" width="100%" height="380" src="' + response.link + '" frameborder="0" allowFullScreen>',
                                    '</iframe>',
                                '</div>'
                            ].join('');
                        }
                        else {
                            preview = [
                                '<div style="height:380px;background-color: black">',
                                    '<center><label style="margin-top:190px; font-size: xx-large; color: white">' + gettext("Preview is not supported") + '</label></center>',
                                '</div>',
                            ].join('');
                        }
                    }

                    var pathAbsence = (response.technical_support.id === 1 || response.technical_support.id === 4 || response.technical_support.id === 5) ? "hidden" : "";
                    var linkAbsence = (response.technical_support.id === 2 || response.technical_support.id === 3) ? "hidden" : "";

                    var pathElement = "";
                    if (response.technical_support.alias === "document"){
                        pathElement = '<a href="' + response.path + '" class="btn btn-primary">' + gettext('Download') + ' <span class="fa fa-download"></span></a>';
                    }
                    else if (response.technical_support.alias === "video") {
                        pathElement = '<a href="' + response.path + '" target="_blank" class="btn btn-danger">' + gettext('Attend') + ' <span class="fa fa-play-circle"></span></a>';
                    }

                    var linkElement = "";
                    if (response.technical_support.alias === "youtube_video" || response.technical_support.alias === "vimeo_video" ) {
                        linkElement = '<a href="' + response.link + '" target="_blank" class="btn btn-danger">' + gettext('Attend') + ' <span class="fa fa-play-circle"></span></a>';
                    }
                    else if (response.technical_support.alias === "shared_link" ) {
                        linkElement = '<a href="' + response.link + '" target="_blank" class="btn btn-success">' + gettext('Follow') + ' <span class="fa fa-hand-o-up"></span></a>';
                    }

                    var detectBrokenLink = "";
                    if (pathAbsence === "hidden") {
                        detectBrokenLink = '<button data-link="' + response.link + '" class="btn btn-info btn-sm detect-broken-link">' + gettext('Validate') + '</button>';
                    }
                    else {
                        detectBrokenLink = '<button data-link="' + baseURL + response.path + '" class="btn btn-info btn-sm detect-broken-link">' + gettext('Validate') + '</button>';
                    }
                    
                    var html = [
                        '<h3 id="#material_'+ response.id +'">' + response.title + '<span ><small>',
                                '<div class="btn-group pull-right">',
                                    '<button data-material="' + response.id + '" class="btn btn-danger delete-material"><span class="fa fa-trash"></span aria-hidden="true"> ' + gettext("Delete") + '  </button>',
                                '</div>',
                            '</small><span>',
                        '</h3>',
                        '<hr class="service-hr">',
                        '<div class="row">',
                            '<div class="col-sm-12 col-md-12 col-lg-12 col-xs-12" style="min-height:250px">',
                                preview,
                            '</div>',
                        '</div>',
                        '<hr class="service-hr" />',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Format") + '</label>',
                            '</div>',    
                            '<div class="col-sm-8 col-md-8">',
                                response.extension,
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Description") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                response.description,
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Dependencies") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                response.software_dependencies,
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Type of material") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                response.technical_support.type,
                            '</div>',
                        '</div>',
                        '<div class="row ' + pathAbsence + '">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Resource path") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                pathElement,
                            '</div>',
                        '</div>',
                        '<div class="row ' + linkAbsence + ' ">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Shared link") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                linkElement,
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Is it visible?") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                (!!response.visible === true) ? gettext('Yes'): gettext('No'),
                            '</div>',
                        '</div>',
                        '<div class="row">',
                            '<div class="col-sm-4 col-md-4 col-md-4 col-xs-4">',
                                '<label>' + gettext("Detect broken link") + '</label>',
                            '</div>',
                            '<div class="col-sm-8">',
                                detectBrokenLink,
                            '</div>',
                        '</div>'
                    ].join('');
                    $("#preview-material").html(html);

                    var height = parseInt($("#preview-material").css("height").replace("px","")) + 350;
                    $(".platform-info-box").css("min-height", height + "px");
                },
                error: function (response) {
                },
                complete: function () {
                }
            });
        },
        //
        // Delete a technical material of service
        //
        deleteServiceTechnicalMaterial: function (url, successURL) {
            $.ajax({
                url: url,
                type: "DELETE",
                beforeSend: function (xhr, settings) {
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function (response) {
                    console.info(gettext("OK"));
                },
                error: function (response) {
                    console.error(gettext("Error"));
                },
                complete: function () {
                    location.href = successURL;
                }
            });
        },
        //
        // Load categories as tree
        //
        loadTreeCategories: function (targetElement) {
            $.ajax({
                type: 'GET',
                url: $(targetElement).data('resource'),
                data: { level: 0 },
                headers: { "accept": "application/json", "content-type": "application/json" },
                contentType: 'application/json',
                success: function (response) {
                    var options = '';
                    var data = response.results;
                    var startList = '<ul><li>';
                    var startListInvisible = '<ul><li class="collapsed">';
                    var endList = '</li></ul>';
                    for (var root in data) {
                        var childs = data[root].children;
                        options += [
                            ((childs.length > 0) ? startListInvisible : startList),
                            '<input type="checkbox" id="category-' + data[root].id + '" name="category-' + data[root].id + '" data-id="' + data[root].id + '" data-name="category-' + data[root].id + '"/>',
                            '<label for="category-' + data[root].id + '" class="tree-items padding-left-5"> ' + data[root].title + '</label>',
                        ].join('');

                        for (var i in childs) {
                            var leafs = childs[i].children;
                            options += [
                                ((leafs.length > 0) ? startListInvisible : startList),
                                '<input type="checkbox" id="category-' + childs[i].id + '" name="category-' + childs[i].id + '" data-id="' + childs[i].id + '" data-name="category-' + childs[i].id + '"/>',
                                '<label for="category-' + childs[i].id + '" class="tree-items padding-left-5"> ' + childs[i].title + '</label>',
                            ].join('');


                            for (var j in leafs) {
                                options += [
                                    startList,
                                        '<input type="checkbox" id="category-' + leafs[j].id + '" name="category-' + leafs[j].id + '" data-id="' + leafs[j].id + '" data-name="category-' + leafs[j].id + '"/>',
                                            '<label for="category-' + leafs[j].id + '" class="tree-items padding-left-5"> ' + leafs[j].title + '</label>',
                                    endList
                                ].join('');
                            }
                            options += endList;
                        }
                        options += endList;
                    }
                    $(targetElement).append(options);
                    $(targetElement).tree({
                        collapsible: true,
                        dnd: false,
                        onCheck: {
                            node: 'expand'
                        },
                        onUncheck: {
                            node: 'collapse'
                        }
                    });
                    $(targetElement).css('border', 'none');
                    $(".daredevel-tree-anchor").css("margin-top", '4px');
                },
                error: function (response) {
                    console.error(response);
                },
                complete: function () {
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