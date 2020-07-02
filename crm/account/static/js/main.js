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