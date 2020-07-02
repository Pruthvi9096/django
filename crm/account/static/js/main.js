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

// $(document).ready(function () {
//     $('.link-formset').formset({
//         addText: 'add link',
//         deleteText: 'remove',
//         prefix: '{{ formset.prefix }}'
//     });
// });

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
}