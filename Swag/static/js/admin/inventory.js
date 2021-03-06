$(document).ready(function () {
    var swag_table = $('#swag_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 10,
        "order": [[1, 'desc']],
        "ajax": {
            url: "/swag",
            type: 'GET'
        },
        "columnDefs": [
            {
                className: 'control',
                orderable: false,
                targets: -1
            },
            {
                "targets": 3,
                orderable: false,
                width: "47px",
                data: null,
                "defaultContent": '<div class="btn-group pull-right" role="group"><button title="Edit" class="btn btn-primary"><i class="fa fa-edit"></i></button></div>'
            }
        ],
        "columns": [
            {"data": "name", "title": "Product"},
            {"data": "description", "title": "Description"},
            {"data": "price", "render": cost, "title": "Price"},
            {"data": null}
        ]
    });

    var items_table = $('#items_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 7,
        "order": [[0, 'desc']],
        "ajax": {
            url: "/items",
            type: 'GET'
        },
        "columnDefs": [
            {
                className: 'control',
                orderable: false,
                targets: -1
            },
            {
                "targets": 5,
                orderable: false,
                width: "75px",
                data: null,
                "defaultContent": '<div class="btn-group pull-right" role="group"><button title="Edit" class="btn btn-primary"><i class="fa fa-edit"></i></button><button title="Stock" class="btn btn-secondary"><i class="fa fa-archive"></i></button></div>'
            }
        ],
        rowGroup: {
            dataSrc: 'product.name'
        },
        "columns": [
            {"data": "product.name", "title": "Image", "visible": false},
            {"data": "item_id", "visible": false},
            {"data": "image", "render": image, "title": "Image"},
            {"data": "color", "render": color, "title": "Color"},
            {"data": "stock", "title": "Stock"},
            {"data": null}
        ]
    });

    $('#swag_table tbody').on('click', 'button', function () {
        var data = swag_table.row($(this).parents('tr')).data();

        $('#product-id').val(data.swag_id);
        $('#product-name').val(data.name);
        $('#description-text').val(data.description);
        $('#category-name').val(data.category);
        $('#price-value').val(data.price);

        $('#swagEdit').modal('toggle');
    });

    $('#items_table tbody').on('click', 'button', function () {
        var data = items_table.row($(this).parents('tr')).data();
        if ($(this).attr('title') === "Edit") {
            // Fill fields
            $('#color-text').val(data.color);
            $('#image-url').val(data.image);
            $('#item-product-id').val(data.product.swag_id);

            // Show Modal
            $('#itemEdit').modal('toggle');
        } else if ($(this).attr('title') === "Stock") {
            function template(size, value, stock_id) {
                return "<div id='size-" + size + "' class='form-group'>\n" +
                    "<label for='size-" + size + "-stock' class='col-form-label'>" + size + ":</label>\n" +
                    "<input type='text' value='" + value + "' class='form-control' id='" + stock_id + "'>\n" +
                    "</div>";
            }

            $.ajax({
                url: "/stock/" + data.item_id,
                success: function (data) {
                    $('#sizes').empty();

                    // Append Sizes for Stock
                    var stock_items = data['data'];
                    for (var index = 0; index < stock_items.length; ++index) {
                        $('#sizes').append($.parseHTML(template(stock_items[index].size, stock_items[index].stock, stock_items[index].stock_id)));
                    }

                    // Show Modal
                    $('#itemStock').modal('toggle');
                },
                error: function (data) {

                }

            });
        }
    });

    $('#updateSwag').click(function () {
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
        swag_table.ajax.reload();
        $('#swagEdit').modal('toggle');
    });

    $('#updateItem').click(function () {
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
        items_table.ajax.reload();
        $('#itemEdit').modal('toggle');
    });

    $('#updateStock').click(function () {
        var returnData = {};
        $('#sizes').children().children('input').each(function () {
            returnData[$(this).attr('id')] = $(this).val();
        });

        $.ajax({
            url: "/update/stock",
            dataType: 'json',
            data: returnData,
            method: "POST"
        });
        items_table.ajax.reload();
        $('#itemStock').modal('toggle');
    });
});
