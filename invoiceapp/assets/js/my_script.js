// MyjavaScript
$(document).ready(function() {
    $('#myModal').on('shown.bs.modal', function () {
      $('#myInput').trigger('focus')
    });
    $(document).on('change', '#id_item_type', function(){
        var selected = $(this).val();
        var parent = $(this).closest('.item-form');
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
            total_amount =0,
            rate = parent.find('.item-rate').val(),
            hours = parent.find('.total-hours').val(),
            product = parseFloat(rate*hours);
        parent.find('.total-amount').val(product);
        // Get total amount of all item forms
        $('.total-amount').each(function(){
            total_amount += parseFloat($(this).val());
        });
        $('.sub-total').val(total_amount);
        $('.invoice-total').val(total_amount);
    });
    // Get total amount of all item forms
    $(document).on('keyup', '.amount', function(){
        var total_amount = 0;
        $('.amount').each(function(){
            total_amount += parseFloat($(this).val());
          })
        $('.sub-total').val(total_amount);
        $('.invoice-total').val(total_amount);
    });
    $(document).on('keyup', '.less', function(){
        var subtotal = $('.sub-total').val(),
            less = $(this).val(),
            total = parseFloat(subtotal-less);
        $('.invoice-total').val(total);
    });
    // Validate Form
    var orders = [];
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

        if($(".item-form").length && itemForm.valid()){
            itemForm.each(function(index, item){
                var item_data = {};
                $(item).serializeArray().map(function(x){item_data[x.name] = x.value;});
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
                $('create-invoice').reset();
            })
        }
    });
});
