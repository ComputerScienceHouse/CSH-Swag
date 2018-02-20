$(document).ready(function () {

    $('#leaveReview').click(function () {
        $('#postReview').modal('toggle');
    });

    $('#submitReview').click(function () {
        $.ajax({
            url: "/new/review",
            data: {
                "item-id": $('#item-id').val(),
                "rating": $('#rating').val(),
                "review-text": $('#review-text').val()
            },
            method: "PUT"
        });
        $('#postReview').modal('toggle');
    });

});