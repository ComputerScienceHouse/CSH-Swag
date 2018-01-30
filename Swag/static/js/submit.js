$('#updateSwag').click(function () {
    console.log("Button Pressed");
    $.ajax({
        url: "/update/swag",
        data: {
            "product-name": $('#product-name').val(),
            "description-text": $('#description-text').val(),
            "category-name": $('#category-name').val(),
            "price-value": $('#price-value').val()
        },
        method: "POST"
    });
    $('#swagEdit').modal('toggle');
});