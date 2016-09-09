/**
 * Module:      JS Wizard for guided assistance (network of services)
 * Dependency:  jQuery
 * Company:     Singular Logic S.A.
 * Author:      Panagiotis Athanasoulis
 * Email:       pathanasoulis@ep.singularlogic.eu
 * License:     Apache 2.0
 */

var GuidedWizard = GuidedWizard || (function () {
    // private variables
    var prevElement = null;
    var currElement = null;
    var nextElement = null;
    var currStep    = null;
    var nextStep    = null;
    var progress    = 1;
    var categoryID  = null;
    var consumerID  = $("#target-consumer").data('target');
    var totalSteps  = $("#accordion").children().length;

    // elements
    var nextStepBtnElement      = $("#wizard-next-step");
    var previousStepBtnElement  = $("#wizard-previous-step");
    var finalStepElement        = $("div#wizard-final-step");
    var progressBarElement      = $('.progress-bar');
    var progressBarInfoElement  = $("#progress-bar-info");
    var servicesTableElement    = $(".services-table");
    var badgeElement            = $(".total-services");
    var goNasBtn                = $("#return-nas-page");

    var endpoints  = {
        'load_services': null,
        'load_temporary_setup': null,
        'load_services_via_keywords': null,
        'submit_selected_services': null,
        'service_consumer_configuration': null
    }

    var panelSettings = {
        "active": {
            "color": '#51A951',
            "background-color": '#fff',
            'panel-class': 'panel-custom-success'
        },
        'inactive': {
            "color": '#fff',
            "background-color": '#51A951',
            'panel-class': 'panel-default'
        }
    };

    var translation = {
        "label_human_based":    "Human-based",
        "label_machine_based":  "Machine-based",
        'label_cost_free':      'FREE',
        'label_yes':            "YES",
        'label_no':             "NO"
    };

    
    //private methods
    var yieldProgress = function (current, total) {
        progress = Math.ceil(current * 100 / total);
        progressBarElement.css('width', progress + '%').attr('aria-valuenow', progress);
        progressBarInfoElement.text(progress + '%');
        return progress;
    };

    var nextBtnShow = function () {
        nextStepBtnElement.removeClass('hidden');
    };

    var nextBtnHide = function () {
        nextStepBtnElement.addClass('hidden');
    };

    var previousBtnShow = function () {
        previousStepBtnElement.removeClass('hidden');
    };

    var previousBtnHide = function () {
        previousStepBtnElement.addClass('hidden');
    };

    var selectServiceListShow = function () {
        servicesTableElement.removeClass('hidden');
        $("#steps").removeClass('hidden');
        $(".finalize-services-table").addClass('hidden');
        $("#final-step").addClass('hidden');
        goNasBtn.removeClass('hidden');
    };

    var previewServiceListShow = function () {
        //$(".services-table").addClass('hidden');
        servicesTableElement.addClass('hidden');
        $("#steps").addClass('hidden');
        $(".finalize-services-table").removeClass('hidden');
        $("#final-step").removeClass('hidden');
        goNasBtn.removeClass('hidden');
    };

    var panelColorize = function (oldElement, newElement) {
        oldElement.removeClass('in').addClass('collapse');
        oldElement.parent().removeClass(panelSettings['active']['panel-class']).addClass(panelSettings['inactive']['panel-class']);
        oldElement.parent().find(badgeElement).css('color', panelSettings['inactive']['color']).css('background-color', panelSettings['inactive']['background-color']);
        newElement.addClass('in').removeClass('collapse');
        newElement.parent().addClass(panelSettings['active']['panel-class']).removeClass(panelSettings['inactive']['panel-class']);
        newElement.parent().find(badgeElement).css('color', panelSettings['active']['color']).css('background-color', panelSettings['active']['background-color']);
    };

    var setOpenStep = function (current) {
        $("div." + panelSettings['active']['panel-class']).each(function () {
            $(this).removeClass(panelSettings['active']['panel-class']).addClass(panelSettings['inactive']['panel-class']);
        });
        current.parent().parent().parent().addClass(panelSettings['active']['panel-class']).removeClass(panelSettings['inactive']['panel-class']);
    };

    var loadCategoriesList = function () {
        // categories
        var initList = [];
        $(".in .child-category:checked").each(function (i) {
            initList.push($(this).data().id);
        });
        return initList;
    }

    var randomloadCategoriesList = function (element) {
        var initList = [];
        element.find($(".child-category:checked")).each(function (i) {
            initList.push($(this).data().id);
        });
        return initList;
    }

    var loadServicesList = function loadServicesList(categoriesList, elem) {
        var loading = new AjaxView($('#current-step-services'));
        var payload = { "categories": categoriesList, 'consumer_id': consumerID };

        $.ajax({
            type: 'POST',
            url: endpoints['load_services'],
            data: JSON.stringify(payload),
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {                
                $('.finalize-services-table').bootstrapTable('destroy');
                $('.services-table').bootstrapTable('destroy');
                $('.services-table').bootstrapTable({ data: response["servicesList"] });
                $('.fixed-table-body').css('height', 'auto');

                $("button").tooltip({ trigger: "hover" });
                $("span").tooltip({ trigger: "hover" });

                if (elem) {
                    elem.parent().find(".total-services").text(response["servicesList"].length);
                }
                else {
                    //$('.in').parent().find(".total-services").text(response["servicesList"].length);
                    $('.in:not(collapse)').parent().find($(".total-services")).text(response["servicesList"].length);
                }
            },
            error: function (response) {
                swal({
                    html: false,
                    title: "Network of assistance services",
                    text: 'Sorry, an error has occurred',
                    type: "warning",
                    confirmButtonText: "Try again!",
                    confirmButtonColor: "#d9534f"
                });
            },
            complete: function () {
                loading.hide();
            }
        });
    }

    var mapContainerHide = function mapContainerHide() {
        $("#map-container").addClass('hidden');
    }

    var autoHeight = function autoHeight() {
        $('.panel-collapse').each(function (index) {
            $(this).css('height', 'auto');
        });
    };

    var pushTemporalService = function pushTemporalService(payload) {
        var loading = new AjaxView($('#current-step-services'));
        loading.show();

        $.ajax({
            type: 'POST',
            url: endpoints['load_temporary_setup'],
            data: JSON.stringify(payload),
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {
            },
            error: function (response) {
                swal({
                    html: false,
                    title: "Network of assistance services",
                    text: 'Sorry, an error has occurred',
                    type: "warning",
                    confirmButtonText: "Try again!",
                    confirmButtonColor: "#d9534f"
                });
            },
            complete: function () {
                loading.hide();
            }
        });
    }

    var popTemporalService = function popTemporalService(payload) {
        var loading = new AjaxView($('#current-step-services'));
        loading.show();

        $.ajax({
            type: 'DELETE',
            url: endpoints['load_temporary_setup'],
            data: JSON.stringify(payload),
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {
            },
            error: function (response) {
                swal({
                    html: false,
                    title: "Network of assistance services",
                    text: 'Sorry, an error has occurred',
                    type: "warning",
                    confirmButtonText: "Try again!",
                    confirmButtonColor: "#d9534f"
                });
            },
            complete: function () {
                loading.hide();
            }
        });
        return true;
    }

    var loadTemporalServices = function loadTemporalServices() {
        var loading = new AjaxView($('#current-step-services'));

        $.ajax({
            type: 'GET',
            url: endpoints['load_temporary_setup'],
            data: {consumer_id: consumerID},
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {

                console.log(response);

                var tbody = "";
                var catAlert = 1;

                if (response["servicesList"].length > 0) {
                    for (var i in response["servicesList"]) {
                        if (response["servicesList"][i]['services'].length > 0) {
                            for (var s in response["servicesList"][i]['services']) {
                                var type = (response["servicesList"][i].type == 'H') ? "Human-based" : "Machine-based";
                                var location = (response["servicesList"][i].location_constraint == 1) ? "<button class='btn btn-link nas-coordinates-btn'><span class='fa fa-globe fa-lg text-info'></span></button>" : "-";
                                var price = (response["servicesList"][i].price == 0) ? 'FREE' : response["servicesList"][i].price + ' (' + response["servicesList"][i].unit + ')';
                                var selected = '';

                                if (response['servicesList'][i].temp_selected == false) {
                                    selected += [
                                        '<button class="btn btn-success btn-xs nas-submit-service" data-action="" data-resource="" data-service-id="' + response["servicesList"][i]['services'][s].id + '">',
                                        '<i class="fa fa-check"></i> ',
                                        '<span> Purchase</span>',
                                        '</button>'
                                    ].join('');
                                }
                                else {
                                    selected += [
                                        '<button class="btn btn-info btn-xs nas-submit-service" data-action="' + response["servicesList"][i]['services'][s].submit_service_url + '" data-resource="' + response["servicesList"][i]['services'][s].service_config_url + '" data-service-id="' + response["servicesList"][i]['services'][s].id + '">',
                                            '<span data-placement="bottom" title="Purchase the ' + response["servicesList"][i]['services'][s].title  + ' service"> Purchase</span>',
                                        '</button>'
                                    ].join('');
                                }

                                tbody += [
                                    '<tr>',
                                    '<td class="custom-aod-table-td" data-href="#cat' + response["servicesList"][i].category.id + '"> ',
                                        '<span class="fa fa-check-circle text-success"></span> ' + response["servicesList"][i].category.title,
                                    '</td>',
                                    '<td class="custom-aod-table-td">' + response["servicesList"][i]['services'][s].title,
                                        '<span class="text-muted preview-service"></span>',
                                    '</td>',
                                    '<td class="custom-aod-table-td text-center">',
                                        '<button class="btn btn-link nas-config-btn" data-url="' + response["servicesList"][i]['services'][s].details_url + '" data-service-id="' + response["servicesList"][i]['services'][s].id + '" data-placement="bottom" title="Access the service configuration\n that provider suggests">',
                                        '<span class="fa fa-cogs fa-lg"></span></button>',
                                    '</td>',
                                    '<td class="text-center custom-aod-table-td">' + selected + '</td>',
                                    '</tr>'
                                ].join('');
                            }
                        }
                        else {
                            catAlert = 0;
                            var selected = [
                                        '<button class="btn btn-default btn-xs final-step-select-service" data-href="#cat' + response["servicesList"][i].category.id + '">',
                                            '<span data-placement="bottom" title="Access the \n' + response["servicesList"][i].category.title + ' category"> Select service</span>',
                                        '</button>'
                            ].join('');

                            tbody += [
                                    '<tr class="additional-services">',
                                    '<td class="custom-aod-table-td" data-href="#cat' + response["servicesList"][i].category.id + '"><span class="fa fa-exclamation-circle text-danger"></span> ' + response["servicesList"][i].category.title + '</td>',
                                    '<td class="custom-aod-table-td">-</td>',
                                    '<td class="custom-aod-table-td text-center">-</td>',
                                    '<td class="text-center custom-aod-table-td">' + selected + '</td>',
                                    '</tr>'
                            ].join('');
                        }
                    }
                }
                else {
                    catAlert = 0;
                    tbody = [
                        '<tr>',
                            '<td colspan="4" class="text-center custom-aod-table-td">No services selected. Navigate in the previous steps to select some services!<td>',
                        '</tr>'
                    ].join('');
                }
                // append data on tbody element
                $("#finalize-services-body").empty().append(tbody);

                if (catAlert == 0) {
                    categoriesAlert();
                }

                $("button").tooltip({ trigger: "hover" });
                $("span").tooltip({ trigger: "hover" });
            },
            error: function (response) {
                swal({
                    html: false,
                    title: "Network of assistance services",
                    text: 'Sorry, an error has occurred',
                    type: "warning",
                    confirmButtonText: "Try again!",
                    confirmButtonColor: "#d9534f"
                });
            },
            complete: function () {
                loading.hide();
            }
        });

        return true;
    }

    var keywordsResult = function keywordsResult(input) {
        var loading = new AjaxView($('.search-services-table'));
        loading.show();

        $('.search-services-table').bootstrapTable('destroy');

        $.ajax({
            type: 'POST',
            url: endpoints['load_services_via_keywords'],
            data: JSON.stringify({ keywords: input, consumerID: consumerID }),
            async: false,
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {
                $('.search-services-table').bootstrapTable({ data: response["data"] });
                $('.fixed-table-body').css('height', 'auto');
                $("#results-number").text(response["data"].length);
                $("button").tooltip({ trigger: "hover" });
                $("span").tooltip({ trigger: "hover" });
            },
            error: function (response) {
                console.error("Error in services' retrieval");
            },
            complete: function () {
                loading.hide();
            }
        });
        return true;
    }

    var categoriesAlert = function categoriesAlert() {
        var text = "You have not selected services for all categories. If you want to declare more services as interesting or purchase more, please click on Select service button of the corresponding category.";

        swal({
            html: false,
            title: "Network of assistance services",
            text: text,
            type: "info",
            confirmButtonText: "Confirm",
            confirmButtonColor: "#428bca"
        });
    }

    var submitSelectedServices = function submitSelectedServices(serviceID) {
        var loading = new AjaxView($('.services-table'));
        loading.show();
        var payload = { serviceID: serviceID, consumerID: consumerID };
        var id = -1;

        $.ajax({
            type: 'POST',
            url : endpoints['submit_selected_services'],
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            data: JSON.stringify(payload),
            async: false,
            headers: {"Accept": "application/json"},
            contentType: 'application/json',
            success: function (response) {
                id = response.id;
            },
            error: function (response) {
                swal({
                    html: false,
                    title: "Network of assistance services: installation steps",
                    text: 'Sorry, an error has occurred',
                    type: "warning",
                    confirmButtonText: "Try again!",
                    confirmButtonColor: "#d9534f"
                });
            },
            complete: function () {
                loading.hide();
            }
        });
        return id;
    }

    var retrieveEditableConfiguration = function retrieveEditableConfiguration(url) {
        $.ajax({
            type: 'GET',
            url: url,
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            contentType: 'application/json',
            success: function (response) {
                var tbody = "";
                if (response.configuration.length > 0) {
                    for (var i in response.configuration) {
                        if (i > 0) { tbody += '<br>'; }
                        tbody += [
                            '<div class="row" data-id="' + response.configuration[i]["id"] + '" >',
                                '<div class="col-sm-4 col-xs-12 col-md-4 col-lg-4">',
                                    '<label class="pull-right config-parameter" id="' + response.configuration[i]["id"] + '" >' + response.configuration[i]["parameter"] + '</label>',
                                '</div>',
                                '<div class="col-sm-8 col-xs-12 col-md-8 col-lg-8">',
                                    '<input type="text" id="' + response.configuration[i]["id"] + '" class=" config-value form-control pull-left" value="' + response.configuration[i]["value"] + '" />',
                                '</div>',
                            '</div>',
                        ].join('');
                    }
                }
                else {
                    tbody += [
                        '<div class="col-sm-12 col-xs-12 col-md-12 col-lg-12">',
                            '<span>No configuration has been set by service provider!</span>',
                        '</div>'
                    ].join('');
                }
                $('#update-configuration').empty().append(tbody);
            },
            error: function (response) {
                console.error(response);
            },
            complete: function () {
            }
        });
    }

    var retrieveConfiguration = function retrieveConfiguration(url) {
        $.ajax({
            type: 'GET',
            url: url,
            beforeSend: function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            headers: {"Accept":'application/json'},
            contentType: 'application/json',
            success: function (response) {
                var tbody = "";

                if (response.configuration.length) {
                    for (var i in response.configuration) {
                        tbody += [
                            '<tr>',
                            '<td class="custom-aod-table-td">' + response.configuration[i]["parameter"] + '</td>',
                            '<td class="custom-aod-table-td">' + response.configuration[i]["value"] + '</td>',
                            '</tr>'
                        ].join('');
                    }
                }
                else {
                    tbody += [
                        '<tr>',
                        '<td colspan="2" class="custom-aod-table-td text-center">No configuration has been set by service provider!</td>',
                        '</tr>'
                    ].join('');
                }

                //if (response.data.length > 0) {
                //    for (var i in response.data) {
                //        tbody += [
                //            '<tr>',
                //            '<td class="custom-aod-table-td">' + response.data[i]["fields"]["parameter"] + '</td>',
                //            '<td class="custom-aod-table-td">' + response.data[i]["fields"]["value"] + '</td>',
                //            '</tr>'
                //        ].join('');
                //    }
                //}
                //else {
                //    tbody += [
                //        '<tr>',
                //        '<td colspan="2" class="custom-aod-table-td text-center">No configuration is provided!</td>',
                //        '</tr>'
                //    ].join('');
                //}
                $('#configuration-table-body').empty().append(tbody);
            },
            error: function (response) {
                console.error(response);
            },
            complete: function () {
            }
        });
    }

    var modalAction = function modalAction(title, content, action, f_action) {
        bootbox.dialog({
            title: title,
            message: content,
            buttons: {
                main: {
                    label: action,
                    className: "btn btn-primary",
                    callback: f_action
                }
            },
            closeButton: true,
            onEscape: function () {
                window.close();
            },
            keyboard: true,
        });
    }

    var modalActionsPost = function modalActionsPost(title, content, cancel, confirm, f_cancel, f_success) {
        bootbox.dialog({
            title: title,
            message: content,
            buttons: {
                danger: {
                    label: cancel,
                    className: "btn btn-danger",
                    callback: f_cancel
                },
                main: {
                    label: confirm,
                    className: "btn btn-success",
                    callback: f_success
                }
            },
            closeButton: true,
            onEscape: function () {
                window.close();
            },
            keyboard: true,
        });
    }



    // public methods
    return {
        setURLs: function (loadServicesURL, loadTemporaryServicesURL, searchServicesByKwdsURL, submitSelectedServicesURL, serviceConsumerConfigurationURL) {
            endpoints['load_services']                  = loadServicesURL;
            endpoints['load_temporary_setup']           = loadTemporaryServicesURL;
            endpoints['load_services_via_keywords']     = searchServicesByKwdsURL;
            endpoints['submit_selected_services']       = submitSelectedServicesURL;
            endpoints['service_consumer_configuration'] = serviceConsumerConfigurationURL;
        },
        customize:  function (activeColor, activeBgColor, activePanel, inactivePanel) {

            $("#accordion").find($('.panel')).removeClass('panel-success').removeClass('panel-custom-success');

            panelSettings["active"]["color"] = activeColor;
            panelSettings["active"]["background-color"] = activeBgColor;
            panelSettings["active"]["panel-class"] = activePanel;

            panelSettings["inactive"]["color"] = activeBgColor;
            panelSettings["inactive"]["background-color"] = activeColor;
            panelSettings["active"]["panel-class"] = inactivePanel;
        },
        init:       function () {
            // Init the wizard
            $('.fixed-table-body').css('height', 'auto');
            progress = yieldProgress(1, totalSteps);
            loadServicesList(loadCategoriesList());
            mapContainerHide();
        },
        next:       function () {
            // Proceed to next step
            currElement = $("div.in");
            categoryID  = currElement.data('id');
            currStep = currElement.data('step');
            autoHeight();
            mapContainerHide();

            switch ($("div[data-step='" + (currStep + 1) + "']").length) {
                case 0:
                    $('.services-table').bootstrapTable('destroy');
                    nextElement = finalStepElement;
                    progress = yieldProgress(totalSteps, totalSteps);
                    previousBtnShow();
                    nextBtnHide();
                    goNasBtn.removeClass('hidden');
                    break;
                case 1:
                    nextElement = $("div[data-step='" + (currStep + 1) + "']");
                    progress = yieldProgress(currStep + 1, totalSteps);
                    previousBtnShow();
            }

            // manage custom wizard (collapse or no divisions)
            panelColorize(currElement, nextElement);
            
            // load services
            if (progress == 100) {
                nextStepBtnElement.addClass('hidden');
                $(".services-table").addClass('hidden');
                $(".finalize-services-table").removeClass('hidden');
                loadTemporalServices();
                $("#steps").addClass('hidden');
                $("#final-step").removeClass('hidden');
            }
            else {
                //loadInitialServices();
                loadServicesList(loadCategoriesList());
            }
        },
        back:       function () {
            // Proceed to previous step
            currElement = $("div.in");
            categoryID  = currElement.data('id');
            currStep = currElement.data('step');
            autoHeight();
            mapContainerHide();

            nextBtnShow();
            switch (currStep) {
                case -1:
                    var pr          = finalStepElement.parent().prev();
                    var collapses   = $('div.collapse:not(.in)');
                    prevElement     = pr.find(collapses[collapses.length - 1]);
                    previousBtnShow();
                    selectServiceListShow();
                    break;
                case 1:
                    progress        = yieldProgress(currStep, totalSteps);
                    previousBtnHide();
                    return;
                case 2:
                    prevElement     = $("div[data-step='" + (currStep - 1) + "']");
                    progress        = yieldProgress(currStep - 1, totalSteps);
                    previousBtnHide();
                    break;
                default:
                    prevElement     = $("div[data-step='" + (currStep - 1) + "']");
                    progress        = yieldProgress(currStep - 1, totalSteps);
                    previousBtnShow();
                    break;
            }

            // manage custom wizard (collapse or no divisions)
            panelColorize(currElement, prevElement);
            // load services
            loadServicesList(loadCategoriesList());
        },
        select:     function (element) {
            currelement = $("div.in");
            var step = element.data('href');
            nextElement = $(step);
            currStep = nextElement.data('step');
            mapContainerHide();

            if (step.split('#cat')[1] == 1){
                previousStepBtnElement.addClass('hidden');
            }

            nextBtnShow();
            selectServiceListShow();

            // handle the progress bar
            yieldProgress(currStep, totalSteps);

            // manage custom wizard (collapse or no divisions)
            panelColorize(currelement, nextElement);

            // load services
            loadServicesList(loadCategoriesList());
        },
        random:     function (element) {
            // Access a random step
            nextElement = $(element.attr("href"));
            currStep    = nextElement.data('step');
            nextElement.css('height', 'auto');
            nextElement.addClass('in').removeClass('collapse');
            autoHeight();
            setOpenStep(element);
            mapContainerHide();
            $('.services-table').bootstrapTable('destroy');

            switch (currStep) {
                case -1:
                    progress = yieldProgress(totalSteps, totalSteps);
                    nextBtnHide();
                    previousBtnShow();
                    previewServiceListShow();
                    loadTemporalServices();
                    break;
                case 1:
                    progress = yieldProgress(currStep, totalSteps);
                    nextBtnShow();
                    previousBtnHide();
                    selectServiceListShow();
                    loadServicesList(randomloadCategoriesList(nextElement), nextElement);
                    break;
                default:
                    progress = yieldProgress(currStep, totalSteps);
                    nextBtnShow();
                    previousBtnShow();
                    selectServiceListShow();
                    loadServicesList(randomloadCategoriesList(nextElement), nextElement);
            }
        
            $("a.wizard-nav").each(function () {
                $(this).parent().find($(".badge")).removeClass(panelSettings['active']['panel-class']).addClass(panelSettings['inactive']['panel-class']);
                $(this).parent().find($(".badge")).css('color', panelSettings['inactive']['color']).css('background-color', panelSettings['inactive']['background-color']);
            });
            element.parent().find($(".badge")).addClass(panelSettings['active']['panel-class']).removeClass(panelSettings['inactive']['panel-class']);
            element.parent().find($(".badge")).css('color', panelSettings['active']['color']).css('background-color', panelSettings['active']['background-color']);
        },
        services:   function () {
            mapContainerHide();
            loadServicesList(loadCategoriesList());
        },
        addWishList: pushTemporalService,
        removeWishList: popTemporalService,
        purchase: function (element) {
            // Consumer purchases a service (write configuration and relationship)
            var serviceId = element.data('serviceId');
            var title = "Customize the service configuration";
            var content = '<div id="update-configuration"></div>';
            retrieveEditableConfiguration(element.data('resource'));
            var nasID = submitSelectedServices(serviceId);

            modalAction(title, content, "Proceed to service purchase", function (feedback) {
                if (feedback) {
                    $("#update-configuration").find($(".row")).each(function () {
                        var config = {
                            "nas": nasID,
                            "value": $(this).find($(".config-value")).val(),
                            "parameter": $(this).find($(".config-parameter")).text(),
                            "is_default": 0
                        };
                        $.ajax({
                            type: 'POST',
                            url: endpoints['service_consumer_configuration'],
                            beforeSend: function (xhr, settings) {
                                $.ajaxSettings.beforeSend(xhr, settings);
                            },
                            data: JSON.stringify(config),
                            headers: {"Accept": "application/json"},
                            contentType: 'application/json',
                            success: function (response) {
                            }
                        });
                    });
                }
            });

        },
        viewConfig: function (element) {
            // Load and preview service configuration
            var url = element.data('url');
            var title = "Service configuration that provider offers";
            var content = [
                '<div class="row">',
                    '<div class="col-sm-12 col-xs-12 col-md-12 col-lg-12">',
                        '<table class="configuration-table table table-responsive">',
                            '<thead>',
                                '<tr class="">',
                                    '<th class="custom-aod-table-th">Parameters</th>',
                                    '<th class="custom-aod-table-th">Values</th>',
                                '</tr>',
                            '</thead>',
                            '<tbody id="configuration-table-body"></tbody>',
                        '</table>',
                    '</div>',
                '</div>'
            ].join('');

            retrieveConfiguration(url);

            modalAction(title, content, "Continue", function () { });
        },
        search: keywordsResult
    }
})();