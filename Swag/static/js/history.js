$(document).ready(function () {
    var receipts_table = $('#receipts_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 8,
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
            },
            {
                "targets": 4,
                orderable: false,
                width: "47px",
                data: null,
                "defaultContent": '<div class="btn-group pull-right" role="group"><button title="Edit" class="btn btn-primary"><i class="fa fa-edit"></i></button></div>'
            }
        ],
        "columns": [
            {"data": "receipt_id", "visible": false},
            {"data": "purchased.item.product.name"},
            {"data": "cost", "render": cost},
            {"data": "method", "render": method},
            {"data": null}
        ]
    });
});
