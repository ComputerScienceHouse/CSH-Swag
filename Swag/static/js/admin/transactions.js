$(document).ready(function () {
    var receipts_table = $('#receipts_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 10,
        "order": [[0, 'desc']],
        "ajax": {
            url: "/receipts/all",
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
                width: "47px",
                data: null,
                "defaultContent": '<div class="btn-group pull-right" role="group"><button title="Edit" class="btn btn-primary"><i class="fa fa-edit"></i></button></div>'
            }
        ],
        "columns": [
            {"data": "receipt_id", "visible": false},
            {"data": "purchased.item.product.name"},
            {"data": "cost", "render": cost},
            {"data": "member_uid", "render": member},
            {"data": "method", "render": method},
            {"data": null}
        ]
    });

    var ctx = $("#purchaseMethods");

    var dataset = {};
    var values = [];
    var purchaseMethods = new Chart(ctx, {
        type: 'pie',
        data: dataset
    });
    $.ajax({
        url: "/methods/all",
        method: "GET",
        success: function (data) {
            for (var key in data) {
                values.push(data[key]);
            }

            dataset = {
                datasets: [{
                    data: values,
                    backgroundColor: ["#39cb4a", "#777777", "#00b6ff"]
                }],
                labels: [
                    'Cash',
                    'Check',
                    'Venmo'
                ]
            }

            purchaseMethods = new Chart(ctx, {
                type: 'pie',
                data: dataset
            });
        }
    });

    $('#receipts_table tbody').on('click', 'button', function () {
        var data = receipts_table.row($(this).parents('tr')).data();

        $('#update-receipt-id').val(data.receipt_id);
        $('#update-transaction-item-id').val(data.purchased.stock_id).trigger('change');
        $('#update-receipt-member').val(data.member_uid).trigger('change');
        $('#update-item-quantity').val(data.quantity);
        $('#update-payment-method').val(data.method).trigger('change');

        $('#editReceipt').modal('toggle');
    });

    $('#updateReceipt').click(function () {
        $.ajax({
            url: "/update/receipt",
            data: {
                "receipt-id": $('#update-receipt-id').val(),
                "transaction-item-id": $('#update-transaction-item-id').val(),
                "receipt-member": $('#update-receipt-member').val(),
                "item-quantity": $('#update-item-quantity').val(),
                "payment-method": $('#update-payment-method').val()
            },
            method: "POST"
        });
        receipts_table.ajax.reload();
        $('#editReceipt').modal('toggle');
    });

    $('#createTransaction').click(function () {
        $('#newTransaction').modal('toggle');
    });

    $('#addNewTransaction').click(function () {
        $.ajax({
            url: "/new/transaction",
            dataType: 'json',
            data: {
                "transaction-item-id": $('#transaction-item-id').val(),
                "receipt-member": $('#receipt-member').val(),
                "item-quantity": $('#item-quantity').val(),
                "payment-method": $('#payment-method').val()
            },
            method: "PUT"
        });
        receipts_table.ajax.reload();
        $('#newTransaction').modal('toggle');
    });
});
