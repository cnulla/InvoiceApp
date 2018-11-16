// MyjavaScript
// My Modal
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});
$(document).ready(function() {
    $(document).on('change', '#id_item_type', function(){

        var selected = $(this).val();
        var parent = $(this).closest('.item-form');
        console.log(parent, 'parent');
        console.log(selected, 'change');
        if(selected === 'fixed'){
            var rate = parent.find('.item-rate').attr('disabled', 'disabled'),
                hours = parent.find('.total-hours').attr('disabled', 'disabled'),
                amount = parent.find('.total-amount');
            rate.val('');
            hours.val('');
            amount.val('');
            parent.find('.amount').removeAttr('disabled');
        }
        if(selected === 'hourly'){
            parent.find('.item-rate').removeAttr('disabled');
            parent.find('.total-hours').removeAttr('disabled');
            var amount = parent.find('.amount').attr('disabled', 'disabled');
            amount.val('');
           parent.find('.total-amount').attr('readonly', 'readonly');
        }
    });
    // Add order form button
    $('#add-order').click(function(){
        var url  = $(this).data('url');
        $.get(url, function(data, status){
            $('#myform').append(data);
        });
    });
    // Get the total amount of item type: hourly
    $(document).on('keyup', '.total-hours', function() {
        var parent = $(this).closest('.item-form'),
            product = 0,
            rate = parent.find('.item-rate').val(),
            hours = parent.find('.total-hours').val(),
            product = parseFloat(rate*hours);
        parent.find('.total-amount').val(product);
    });
    $(document).on('change', '#id_amount', function(){
        var amount = $(this).val(),
            subtotal = $('#id_subtotal').val(amount),
            total = $('#id_total').val(parseFloat(amount));
        console.log(total,'total');
    });

    var orders = [];
    // Validate Form
    $('#create-invoice').validate({
        rules: {
            invoice_number: 'required',
            company: 'required'
        }
    });
    $('#itemform').validate();
    // Submit Form
    $('#create-invoice').on('submit', function(e){
        e.preventDefault();
        var form = $(this),
            invoice_data = form.serialize(),
            itemForm = $('.item-form');

        if(itemForm.valid()){
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
        console.log(orders);
        var data = $(this).serializeArray();
        data.push({name: "items", value:  JSON.stringify(orders)});

        if(form.valid()){
            $.ajax({
                url: form.attr('action'),
                data:  data,
                type: 'POST',
                dataType:'json'
            }).done(function(response){
                alert(response)
            }).fail(function(error){
            });
        }

    });
});
