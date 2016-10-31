

$(".decrease-font-size").click(function () {
    fontResize($("body *"), -1);
    return false;
});

$(".increase-font-size").click(function () {
    fontResize($("body *"), +1);
    return false;
});

$(".reset-font-size").click(function () {
    $("body *").css('font-size', "14px");
    return false;
});



function fontResize(element, diff) {
    var tempFontSize = element.css('font-size').replace(/\D/g, '');
    var updatedFontSize = parseInt(tempFontSize) + parseInt(diff);
    updatedFontSize = updatedFontSize.toString() + "px";
    element.css('font-size', updatedFontSize);
}