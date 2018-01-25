function color(data) {
    return "<span class='badge badge-" + data.toLowerCase() + "'>" + data + "</span>";
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
            {"data": "price", "title": "Price"},
            {
                "data": null,
                "render": function (data, type, row) {
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
        "order": [[1, 'desc']],
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
            // Group by office
            dataSrc: 'product.name'
        },
        "columns": [
            {"data": "color", "render": color, "title": "Color"},
            {"data": "image", "title": "Image"},
            {
                "data": null,
                "render": function (data, type, row) {
                    return "";
                }
            }
        ]
    });
});