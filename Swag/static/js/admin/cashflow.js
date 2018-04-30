$(document).ready(function () {
    var cashflow_table = $('#cashflow_table').DataTable({
        "paging": true,
        "lengthChange": false,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "pageLength": 10,
        "order": [[0, 'desc']],
        "ajax": {
            url: "/cashflow/all",
            type: 'GET'
        },
        "columnDefs": [
            {
                className: 'control',
                orderable: false,
                targets: -1
            },
            {
                "targets": 7,
                orderable: false,
                width: "47px",
                data: null,
                "defaultContent": '<div class="btn-group pull-right" role="group"><button title="Edit" class="btn btn-primary"><i class="fa fa-edit"></i></button></div>'
            }
        ],
        "columns": [
            {"data": "flow_id", "visible": false},
            {"data": "datetime"},
            {"data": "reason"},
            {"data": "financial_uid", "render": member},
            {"data": "account_to"},
            {"data": "account_from"},
            {"data": "amount"},
            {"data": null}
        ]
    });

    $('#cashflow_table tbody').on('click', 'button', function () {
        var data = cashflow_table.row($(this).parents('tr')).data();

        $('#update-receipt-id').val(data.receipt_id);
        $('#update-transaction-item-id').val(data.purchased.stock_id).trigger('change');
        $('#update-receipt-member').val(data.member_uid).trigger('change');
        $('#update-item-quantity').val(data.quantity);
        $('#update-payment-method').val(data.method).trigger('change');

        $('#editCashFlow').modal('toggle');
    });

    $('#updateCashFlow').click(function () {
        $.ajax({
            url: "/update/cashflow",
            data: {
                "receipt-id": $('#update-receipt-id').val(),
                "transaction-item-id": $('#update-transaction-item-id').val(),
                "receipt-member": $('#update-receipt-member').val(),
                "item-quantity": $('#update-item-quantity').val(),
                "payment-method": $('#update-payment-method').val()
            },
            method: "POST"
        });
        cashflow_table.ajax.reload();
        $('#editCashFlow').modal('toggle');
    });

    $('#createCashFlow').click(function () {
        $('#newTransaction').modal('toggle');
    });

    $('#addNewCashFlow').click(function () {
        $.ajax({
            url: "/new/cashflow",
            dataType: 'json',
            data: {
                "transaction-item-id": $('#transaction-item-id').val(),
                "receipt-member": $('#receipt-member').val(),
                "item-quantity": $('#item-quantity').val(),
                "payment-method": $('#payment-method').val()
            },
            method: "PUT"
        });
        cashflow_table.ajax.reload();
        $('#newCashFlow').modal('toggle');
    });
});
