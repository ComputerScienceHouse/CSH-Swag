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

    var ctx = $("#purchaseMethods");

    var dataset = []
    $.ajax({
        url: "/methods",
        method: "GET",
        success: function (data) {
            data.forEach(function (method) {
                dataset.add(method)
            });
        }
    });

    data = {
        datasets: [{
            data: dataset,
            backgroundColor: ["#39cb4a", "#00b6ff", "#777777"]
        }],
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Cash',
            'Venmo',
            'Check'
        ]
    }

    var purchaseMethods = new Chart(ctx, {
        type: 'pie',
        data: data
    });
});
