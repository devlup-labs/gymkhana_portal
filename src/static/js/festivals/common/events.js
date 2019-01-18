// $('.carousel .carousel-item').each(function () {
//     var next = $(this).next();
//     if (!next.length) {
//         next = $(this).siblings(':first');
//     }
//     next.children(':first-child').clone().appendTo($(this));
// });
// $(function () {
//     $('.event-info').click(() => {
//         var id = $(this).attr("id");
//         console.log(id);
//     });
// });\
$('.event-info').click((e) => {
    // console.log($("#"+e.target.id).text())

    if($("#"+e.target.id).text() == "Explore..."){
        $("#"+e.target.id).text("Close");
        $("#"+e.target.id+"-info-wrapper"+"").css('display','block');
    }else{
        $("#"+e.target.id).text("Explore...");
        $("#"+e.target.id+"-info-wrapper"+"").css('display','none');
    }
});