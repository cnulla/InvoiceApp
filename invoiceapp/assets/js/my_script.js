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
            parent.find('.amount').removeAttr('readonly');
        }
        if(selected === 'hourly'){
            parent.find('.item-rate').removeAttr('disabled');
            parent.find('.total-hours').removeAttr('disabled');
            var amount = parent.find('.amount').attr('readonly', 'readonly');
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
            total_amount = 0,
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
    //Get total invoice
    $(document).on('keyup', '.amount', function(){
        var items = getItems();
        if(items) {
            calculateTotalInvoiceAmount(items);
        }
    });
    $(document).on('keyup', '.total-hours', function(){
        var items = getItems();
        if(items) {
            calculateTotalInvoiceAmount(items);
        }
    });
    //calculate invoice
    function calculateTotalInvoiceAmount(items) {
        var totalAmount = 0;

        $(items).each(function(index, item){
            var amount = 0;
            if(item.item_type === 'fixed'){
                amount = item.amount;
            }
            if(item.item_type === 'hourly'){
                amount = item.total_amount;
            }
            totalAmount += parseFloat(amount);
            console.log(item);
        });

        $('.sub-total').val(totalAmount);
        $('.invoice-total').val(totalAmount);
        console.log(totalAmount);
    }
    //get items from item form
    function getItems() {
        itemForm = $('.item-form');
        var orders = [];
        itemForm.each(function(index, item){
            console.log(item, 'test');
            var item_data = {};
            $(item).serializeArray().map(function(x){item_data[x.name] = x.value;});
            console.log(item_data, "xx");
            orders.push(item_data);
        });
        console.log('getItems',orders);
        return orders;
    }
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
            itemForm = $('.item-form');
        if($(".item-form").length && itemForm.valid()){
           var orders = getItems();
        }
        // put all values of orders in a span
        $('#orders').val(orders);
        console.log('orders: ', orders);
        var data = $(this).serializeArray();
        data.push({name: "items", value:  JSON.stringify(orders)});
        if(form.valid()){
            console.log(data,'>>>>>>>data');
            $.ajax({
                url: form.attr('action'),
                data:  data,
                type: 'POST',
                dataType:'json'
            }).done(function(response){
                $('create-invoice').reset();
            });
        }
    });
});
