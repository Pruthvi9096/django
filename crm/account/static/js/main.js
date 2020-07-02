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

function deleteOrder(order){
    console.log(order)
    var content = "<h4>Are you sure to delete this order ?</h4><br/>"
    var table = `<table class='table table-sm'><tbody><tr><th>Product</th><th>Date Orderd</th><th>Status</th></tr><tr><td>${order.product}</td><td>${order.date_ordered}</td><td>${order.status}</td></tr></tbody></table>`
    var input = `<input type='hidden' id='delete-order-id' value=${order.id} />`
    $('#order-content').html(content+ table + input);
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