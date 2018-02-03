$('#updateSwag').click(function () {
    console.log("Button Pressed");
    $.ajax({
        url: "/update/swag",
        data: {
            "product-id": $('#product-id').val(),
            "product-name": $('#product-name').val(),
            "description-text": $('#description-text').val(),
            "category-name": $('#category-name').val(),
            "price-value": $('#price-value').val()
        },
        method: "POST"
    });
    $('#swagEdit').modal('toggle');
});

$('#updateItem').click(function () {
    console.log("Button Pressed");
    $.ajax({
        url: "/update/item",
        data: {
            "item-id": $('#item-id').val(),
            "product-id": $('#item-product-id').val(),
            "color-text": $('#color-text').val(),
            "image-url": $('#image-url').val()
        },
        method: "POST"
    });
    $('#itemEdit').modal('toggle');
});