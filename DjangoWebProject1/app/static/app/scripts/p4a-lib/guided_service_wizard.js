/**
 * Module:  Wizard for guided network of services
 * Dependency: jQuery
 * Author:  Panagiotis Athanasoulis
 * email:   pathanasoulis@ep.singularlogic.eu
 * license: Apache 2.0
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


    //private methods
    var yieldProgress = function (current, total) {
        progress = current * 100 / total;
        $('.progress-bar').css('width', progress + '%').attr('aria-valuenow', progress);
        $("#progress-bar-info").text(progress + '%');
        return progress;
    };

    var nextBtnShow = function () {
        $("#wizard-next-step").removeClass('hidden');
    };

    var nextBtnHide = function () {
        $("#wizard-next-step").addClass('hidden');
    };

    var previousBtnShow = function () {
        $("#wizard-previous-step").removeClass('hidden');
    };

    var previousBtnHide = function () {
        $("#wizard-previous-step").addClass('hidden');
    };

    var selectServiceListShow = function () {
        $(".services-table").removeClass('hidden');
        $("#steps").removeClass('hidden');
        $(".finalize-services-table").addClass('hidden');
        $("#final-step").addClass('hidden');
        $("#return-nas-page").removeClass('hidden');
    };

    var previewServiceListShow = function () {
        $(".services-table").addClass('hidden');
        $("#steps").addClass('hidden');
        $(".finalize-services-table").removeClass('hidden');
        $("#final-step").removeClass('hidden');
        $("#return-nas-page").removeClass('hidden');
    };

    var loadCategoriesList = function () {
        // categories
        var initList = [];
        $(".in .child-category:checked").each(function (i) {
            initList.push($(this).data().id);
        });
        return initList;
    }

    var setOpenStep = function (current) {
        $(current).addClass('in').removeClass('collapse');

        $("div.panel-primary").each(function () {
            $(this).removeClass('panel-primary').addClass('panel-default');
        });
        current.parent().parent().parent().removeClass('panel-default').addClass('panel-primary');
    }


    

    // public methods
    return {
        init:       function (totalSteps) {
            progress = yieldProgress(1, totalSteps);
        },
        next:       function (selector, currElement, totalSteps, loadInitialServices, loadTemporalServices) {
            categoryID  = currElement.data('id');
            currStep    = currElement.data('step');

            //switch (nextElement.length) {
            //    case 0:
            //        nextElement = $("div#wizard-final-step");
            //        progress = yieldProgress(totalSteps, totalSteps);
            //        previousBtnShow();
            //        nextBtnHide();
            //        previewServiceListShow
            //        loadTemporalServices();
            //        break;
            //    default:
            //        progress = yieldProgress(currStep + 1, totalSteps);
            //        previousBtnShow();
            //        loadInitialServices();
            //}

            if ($("div[data-step='" + (currStep + 1) + "']").length) {
                nextElement = $("div[data-step='" + (currStep + 1) + "']");
                progress = yieldProgress(currStep + 1, totalSteps);
                previousBtnShow();
                //nextBtnShow();
            }
            else {
                nextElement = $("div#wizard-final-step");
                progress = yieldProgress(totalSteps, totalSteps);
                previousBtnShow();
                nextBtnHide();
                $("#return-nas-page").removeClass('hidden');
            }

            // manage custom wizard (collapse or no divisions)
            currElement.removeClass('in').addClass('collapse');
            currElement.parent().removeClass('panel-primary').addClass('panel-default');
            nextElement.addClass('in').removeClass('collapse');
            nextElement.parent().addClass('panel-primary').removeClass('panel-default');
            
            // load services
            if (progress == 100) {
                selector.addClass('hidden');
                $(".services-table").addClass('hidden');
                $(".finalize-services-table").removeClass('hidden');
                loadTemporalServices();
                $("#steps").addClass('hidden');
                $("#final-step").removeClass('hidden');
            }
            else {
                loadInitialServices();
           }
        },
        previous:   function (selector, currElement, totalSteps, loadInitialServices) {
            categoryID  = currElement.data('id');
            currStep    = currElement.data('step');

            nextBtnShow();
            switch (currStep) {
                case -1:
                    var pr = $("#wizard-final-step").parent().prev();
                    var collapses = $('div.collapse');
                    prevElement = pr.find(collapses[collapses.length - 1]);
                    previousBtnShow();
                    selectServiceListShow();
                    break;
                case 1:
                    progress = yieldProgress(currStep, totalSteps);
                    previousBtnHide();
                    return;
                case 2:
                    prevElement = $("div[data-step='" + (currStep - 1) + "']");
                    progress = yieldProgress(currStep - 1, totalSteps);
                    previousBtnHide();
                    break;
                default:
                    prevElement = $("div[data-step='" + (currStep - 1) + "']");
                    progress = yieldProgress(currStep - 1, totalSteps);
                    previousBtnShow();
                    break;
            }

            // manage custom wizard (collapse or no divisions)
            currElement.removeClass('in').addClass('collapse');
            currElement.parent().removeClass('panel-primary').addClass('panel-default');
            prevElement.addClass('in').removeClass('collapse');
            prevElement.parent().addClass('panel-primary').removeClass('panel-default');

            // load services
            loadInitialServices();
        },
        random:     function (element, totalSteps, loadInitialServices, loadTemporalServices) {
            nextElement = $(element.attr("href"));
            currStep    = nextElement.data('step');
            nextElement.css('height', 'auto');

           
            $('.panel-collapse').each(function (index) {
                $(this).css('height', 'auto');
            });
            setOpenStep(element);

            console.log(loadCategoriesList());

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
                    //return loadCategoriesList();
                    //console.log(loadCategoriesList());
                    //loadServicesList(loadCategoriesList());
                    loadInitialServices();
                default:
                    progress = yieldProgress(currStep, totalSteps);
                    nextBtnShow();
                    previousBtnShow();
                    selectServiceListShow();
                    //return loadCategoriesList();
                    //console.log(loadCategoriesList());
                    //loadServicesList(loadCategoriesList());
                    loadInitialServices();
            }
        }
    }

})();