function updateCount(btn, upvoteCount, help_text) {
    btn.find('.upvoteCount').text(upvoteCount);
    btn.attr('title', help_text);
    btn.attr('data-original-title', help_text);
}

$('.upvote-btn').click(function (e) {
    e.stopImmediatePropagation();
    e.preventDefault();
    var this_ = $(this);
    var upvoteUrl = this_.attr("data-url");
    var upvoteCount = parseInt(this_.attr("data-upvotes"));
    $.ajax({
        url: upvoteUrl,
        method: 'GET',
        data: {},
        success: function (data) {
            if (data.upvoted) {
                upvoteCount++;
                updateCount(this_, upvoteCount, "Remove Upvote");
                this_.attr("data-upvotes", upvoteCount);
            }
            else {
                upvoteCount--;
                updateCount(this_, upvoteCount, "Upvote");
                this_.attr("data-upvotes", upvoteCount);
            }
        },
        error: function (error) {
            console.log(error);
        }
    })
});