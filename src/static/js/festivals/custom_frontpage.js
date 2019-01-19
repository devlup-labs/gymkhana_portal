$('.nav_bars').click(() => {
    if ($('#nav').css('display') == "none") {
        $('#nav').css('display', 'block');
    } else
        $('#nav').css('display', 'none');
})
$('#nav #nav_cross').click(() => {
    if ($('#nav').css('display') == "none") {
        $('#nav').css('display', 'block');
    } else
        $('#nav').css('display', 'none');
})



$(window).on("load", function () {
    $('.loader').delay(3000).fadeOut();
});