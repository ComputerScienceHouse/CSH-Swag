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

function member(data) {
    if (data != null) {
        return "<img class='img-thumbnail table' src='https://profiles.csh.rit.edu/image/" + data + "'>";
    } else {
        return "<img class='img-thumbnail table' src='http://placehold.it/25x25'>";
    }
}

function method(data) {
    if (data != null){
        return "<span class='badge badge-" + data.toLowerCase() + "'>" + data + "&nbsp;<i class='fa fa-check'></i></span>";
    } else {
        return "<i class='fa fa-times' style='color: red'></i>";
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
        "pageLength": 5,
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
        "pageLength": 5,
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

    $('#receipts_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 10,
        "order": [[0, 'desc']],
        "ajax": {
            url: "/receipts",
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
            {"data": "receipt_id", "title": "ID"},
            {"data": "purchased.item.product.name", "title": "Product"},
            {"data": "purchased.size", "title": "Size"},
            {"data": "member_uid", "render": member, "title": "Member"},
            {"data": "method", "render": method,"title": "Method"},
            {
                "data": null,
                "render": function () {
                    return "";
                }
            }
        ]
    });
});