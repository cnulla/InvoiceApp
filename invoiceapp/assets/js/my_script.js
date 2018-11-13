// MyjavaScript
// My Modal
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});
// For CSRF Token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
var csrftoken = getCookie('csrftoken');

// Get the total amount of item type: hourly
$(document).ready(function() {
    $(document).on('change', '#id_total_hours', function() {
        var product = 0;
        var rate = $('#id_rate').val()
        var hours = $('#id_total_hours').val()
        var total = parseFloat(rate*hours)
        $('#id_total_amount').val(total);
    });

// Add order form button
$('#add-order').click(function(){
    var url  = $(this).data('url');
    $.get(url, function(data, status){
        console.log(data, 'data0');
        $('#myform').append(data);
    });
});
});

var InvoiceForm = function(){
    var invoice_number = $('#invoice_number'),
    invoice_description = $('#invoice_description'),
    company = $('#company'),
    payment_status = $('#payment_status'),
    invoice_date = $('#invoice_date'),
    due_date = $('#due_date')

    var orders = [];

    return {
        submit: submit,
    }

    function submit(){

        var invoice_data = $('.create-invoice').serialize();
        var itemForm = $('.item-form');

        itemForm.each(function(index, item){
            console.log(item, 'test');
            var item_data = {};
            $(item).serializeArray().map(function(x){item_data[x.name] = x.value;});
            console.log(item_data, "xx");
            orders.push(item_data);
        });

        var data = {
            invoice_data: invoice_data,
            item_data: orders
        }
        console.log(orders, '>>>>>>>>>>>');
        console.log(data)
        $('input[name="orders"]').val(orders);
        var hidden = document.getElementById('#orders');
        console.log(hidden)

        $.ajax({
            url: '/create-invoice/',
            type: 'POST',
            data: data,
            success: function(resp){
                alert('yey!');
            },
            errors: function(resp){
            }
        });
    }
}();
