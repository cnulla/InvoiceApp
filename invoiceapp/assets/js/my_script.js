// MyjavaScript
// My Modal
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});


$(document).ready(function() {
    // Get the total amount of item type: hourly

    // Add order form button
    $('#add-order').click(function(){
        var url  = $(this).data('url');
        $.get(url, function(data, status){
            $('#myform').append(data);
        });
    });
    $(document).on('change', '.item-form', function() {
        var product = 0,
            rate = $('#id_rate').val(),
            hours = $('#id_total_hours').val(),
            product = parseFloat(rate*hours);
        $('#id_total_amount').val(product);
    });

    var orders = [];
    // Validate Form
    $('#create-invoice').validate({
        rules: {
            invoice_number: 'required',
            company: 'required'
        }
    });
    $('#itemform').validate({
        rules: {
            order_number: 'required',
            order_description: 'required'
        }
    });
    // Submit Form
    $('#create-invoice').on('submit', function(e){
        e.preventDefault();
        console.log('>>>>>>>');
        var form = $(this);
        var invoice_data = form.serialize();
        var itemForm = $('.item-form');

        if(itemForm.valid()) {
            itemForm.each(function(index, item){
            console.log(item, 'test');
            var item_data = {};
            $(item).serializeArray().map(function(x){item_data[x.name] = x.value;});
            console.log(item_data, "xx");
            orders.push(item_data);
        });
    }

        // put all values of orders in a span
        $('#orders').val(orders);

        var data = $(this).serializeArray();
        data.push({name: "items", value:  JSON.stringify(orders)});

        if(form.valid()){
            $.ajax({
                url: form.attr('action'),
                data:  data,
                type: 'POST',
                dataType:'json'
            }).done(function(response){

            }).fail(function(error){
            });
        }
    });
});


