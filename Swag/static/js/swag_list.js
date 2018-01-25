function color(data) {
    return "<span class='badge badge-" + data.toLowerCase() + "'>" + data + "</span>";
}

function image(data) {
    if (data != null) {
        return "<img class='img-thumbnail table' src='" + data + "'>";
    } else {
        return "<img class='img-thumbnail table' src='http://placehold.it/25x25'>";
    }
}


$(document).ready(function () {
    $('#swag_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
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
            }
        ],
        "columns": [
            {"data": "name", "title": "Product"},
            {"data": "description", "title": "Description"},
            {"data": "category", "title": "Category"},
            {"data": "price", "title": "Price"},
            {
                "data": null,
                "render": function () {
                    return "";
                }
            }
        ]
    });

    $('#items_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
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
            }
        ],
        rowGroup: {
            dataSrc: 'product.name'
        },
        "columns": [
            {"data": "product.name", "title": "Image", "visible": false},
            {"data": "image", "render": image, "title": "Image"},
            {"data": "color", "render": color, "title": "Color"},
            {"data": "stock", "title": "Stock"},
            {
                "data": null,
                "render": function () {
                    return "";
                }
            }
        ]
    });
});