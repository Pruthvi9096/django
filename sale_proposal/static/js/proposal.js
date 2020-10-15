$(document).ready(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    
    $('.sale-price, .qty, .discount, .count-balance').on('keyup change', function (e) {
        var line = $(this).closest('tr')
        var sale_price = parseFloat($(line).find('.sale-price').val());
        var qty = parseInt($(line).find('.qty').val());
        var discount = parseFloat($(line).find('.discount').val());
        var subtotal = 0.0
        subtotal = sale_price * qty;
        if (discount) {
            subtotal = subtotal - discount
        }
        $(line).find('.subtotal').val(subtotal);
        var order_line = $(line).attr('data-order-line');
        $.ajax({
            url: `/update_order_line/${order_line}/`,
            method: 'POST',
            headers: {'X-CSRFToken':csrftoken},
            data: {
                'price': parseFloat($(line).find('.sale-price').val()),
                'qty': parseFloat($(line).find('.qty').val()),
                'discount_amount': parseFloat($(line).find('.discount').val()) || 0.00,
                'subtotal': parseFloat($(line).find('.subtotal').val())
            },
            success: function(response) {
                console.log(response);
            }
        })
        var monthlies_amount = 0.0
        var setup_amount = 0.0
        $('.order-line').each(function (index, el) {
            var charge_category = $(el).attr('data-charge-category');
            if (charge_category == 'Monthlies') {
                monthlies_amount += parseFloat($(el).find('.subtotal').val());
            }
            else {
                setup_amount += parseFloat($(el).find('.subtotal').val());
            }
        });
        $('#id_monthlies_amount').val(monthlies_amount)
        $('#id_setup_amount').val(setup_amount)

        var upfront_deposit = $('#id_upfront_deposit').val();
        // var setup_amount = parseFloat($('#id_setup_amount').val());
        // var monthlies_amount = parseFloat($('#id_monthlies_amount').val());
        // var total_amount = setup_amount + monthlies_amount
        var upfront_deposit_amount = 0.0
        if (['other', 'amount'].indexOf(upfront_deposit) != -1) {
            $('#id_display_upfront').closest('div').removeClass('d-none');
            $('#id_display_upfront').prop({ 'required': true }).focus();
            var ufda = parseFloat($('#id_display_upfront').val());
            if (upfront_deposit == 'other') {
                upfront_deposit_amount = setup_amount * (ufda / 100)
            }
            if (upfront_deposit == 'amount') {
                upfront_deposit_amount = ufda;
            }
        }
        else {
            upfront_deposit_amount = setup_amount * (upfront_deposit / 100)
        }
        $('#id_upfront_deposit_amount').val(upfront_deposit_amount || 0.00)
        $('#id_amount_at_execution_of_contract').val(upfront_deposit_amount || 0.00)
        var balance_amount = setup_amount - upfront_deposit_amount;
        $('#id_balance_amount').val(balance_amount || setup_amount);
    });

});