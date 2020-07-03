function updateOrder(id){
    $.ajax({
        url: "/update/"+id,
        data: "",
        success: function (response) {
            $('#order').html(response['form'])
            $('#order-id').val(response['id']);
        }
    });
}

function submitOrder(){
    var form = $('#orderForm')
    $.ajax({
        type:form.attr("method"),
        url: "/saveorder/"+$('#order-id').val(),
        data: form.serialize(),
        success: function (response) {
            if(response['is_form_valid']){
                $('#updateorderModal').modal('toggle');
                window.location.reload();
            }
        }
    });
}

function deleteOrder(order){
    console.log(order)
    $('#product').text(order.product)
    $('#date_ordered').text(order.date_ordered)
    $('#status').text(order.status)
    $('#delete-order-id').val(order.id)
}

function confirmDelete(){
    $.ajax({
        url: "/delete_order/"+$('#delete-order-id').val(),
        data: "",
        success: function (response) {
            if(response['deleted']){
                $('#deleteOrderModal').modal('toggle');
                window.location.reload();
            }
        }
    });

}

function updateCustomer(id) {
    $.ajax({
        url: "/update_customer/"+id,
        data: "",
        success: function (response) {
            console.log(response)
            $('.customer').html(response['form'])
            $('#customer_id').val(response['id']);
        }
    });
}

function saveCustomer() {
    var form = $('#customerForm');
    $.ajax({
        type:form.attr('method'),
        url: "/save_customer/"+$('#customer_id').val(),
        data: form.serialize(),
        success: function (response) {
            if(response['form_is_valid']) {
                console.log("SUCCESS",response);
            }
        }
    });
}

function removeItem(btn){
    var total = $('#id_order_set-TOTAL_FORMS').val();
    total--;
    $('#id_order_set-TOTAL_FORMS').val(total);
    var item = btn.closest('.table').remove()
}

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    newElement.find('.col-sm-1').html('<a href="#" onclick="removeItem(this)" class="closecustom">')
}

// another way for dynamic formset
/* <h3>My Services</h3>
{{ serviceFormset.management_form }}
<div id="form_set">
    {% for form in serviceFormset.forms %}
        <table class='no_error'>
            {{ form.as_table }}
        </table>
    {% endfor %}
</div>
<input type="button" value="Add More" id="add_more">
<div id="empty_form" style="display:none">
    <table class='no_error'>
        {{ serviceFormset.empty_form.as_table }}
    </table>
</div>
<script>
    $('#add_more').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
</script> */