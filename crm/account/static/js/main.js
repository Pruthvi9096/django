function updateOrder(id){
    console.log(id)
    $.ajax({
        url: "/update/",
        data: {'id':id},
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
        url: "/saveorder/?id="+$('#order-id').val(),
        data: form.serialize(),
        success: function (response) {
            if(response['is_form_valid']){
                $('#updateorderModal').modal('toggle');
                window.location.reload();
            }
        }
    });
}