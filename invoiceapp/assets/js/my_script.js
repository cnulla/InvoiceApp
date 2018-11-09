// javaScript
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});

$(document).ready(function() {
    $('#id_total_hours').change(function() {
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
            $('#mydiv').append(data);
        });
    });
});
