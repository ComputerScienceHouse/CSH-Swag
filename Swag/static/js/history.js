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
        "columns": [
            {"data": "receipt_id", "visible": false},
            {"data": "datetime", "title": "Date"},
            {"data": "purchased.item.product.name", "title": "Product"},
            {"data": "cost", "render": cost, "title": "Cost"},
            {"data": "method", "render": method, "title": "Method"}
        ]
    });
});
