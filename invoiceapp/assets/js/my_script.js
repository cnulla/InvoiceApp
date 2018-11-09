// javaScript
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});

$(document).ready(function() {
    $(document).on('change', '#id_total_hours', function() {
        var product = 0;
        var rate = $('#id_rate').val()
        var hours = $('#id_total_hours').val()
        var total = parseFloat(rate*hours)
        console.log(total,'yey')
        $('#id_total_amount').val(total);
    });

    $('#add-order').click(function(){
        var url  = $(this).data('url');
        $.get(url, function(data, status){
            console.log(data, 'data0');
            $('#myform').append(data);
        });
    });

    var orders = [];
    $('#add-invoice').on('click', function(){
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

    });


});

