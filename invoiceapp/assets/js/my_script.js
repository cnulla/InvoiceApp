// MyjavaScript
// My Modal
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});

// Get the total amount of item type: hourly
$(document).ready(function() {
    $(document).on('change', '#id_total_hours', function() {
        var product = 0;
        var rate = $('#id_rate').val()
        var hours = $('#id_total_hours').val()
        var total = parseFloat(rate*hours)
        $('#id_total_amount').val(total);
    });

Add order form button
$('#add-order').click(function(){
    var url  = $(this).data('url');
    $.get(url, function(data, status){
        console.log(data, 'data0');
        $('#myform').append(data);
    });
});

var orders = [];
$('#add-invoice').on('click', function(event){
    var itemForm = $('.item-form');
    console.log('#add-invoice')
    itemForm.each(function(index, item){
        console.log(item, 'test');
        var data = {};
        $(item).serializeArray().map(function(x){data[x.name] = x.value;});
        console.log(data);
        orders.push(data);

    });
    console.log(orders, '>>>>>>>>');
    $('input[name="orders"]').val(orders)

// Submit Invoice Form
    // $(document).on('submit', function(event){
    //     event.preventDefault();
    //     var invoiceForm = $('.create-invoice')
    //     $.ajax({
    //         url: invoiceForm.attr('action')
    //         type: invoiceForm.attr('method'),
    //         data: invoiceForm.serialize(),
    //         success: function(resp){
    //             alert(resp);
    //         },
    //         errors: function(resp){

    //         }
    //     })
    // });
// });

});


var InvoiceForm = function(){
    var invoice_number = $('#invoice_number'),
        invoice_description = $('#invoice_description'),
        company = $('#company'),
        payment_status = $('#payment_status'),
        invoice_date = $('#invoice_date'),
        due_date = $('#due_date')

    return {
        submit: submit
    }

    function submit(){
        var data = $('.create-invoice').serialize();
        $.ajax({
            url: '/create-invoice/',
            type: 'POST',
            data: data,
            success: function(resp){
                console.log(resp)
            },
            errors: function(resp){

            }

        });
    }

}();
