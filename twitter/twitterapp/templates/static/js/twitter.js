console.log($('.btn-outline-danger'))

$('.btn-outline-danger').click(function (e) { 
    e.preventDefault();
    $.ajax({
        url:'unfollow/'+target+'/'+follower,
        data:'',
        success:function(response) {
            console.log("--response--",response)
            if(response['is_unfollowed']) {
                $(el).prev().prop({'disabled':false})
                $(el).prev().text("Follow")
                $(el).remove()
            }
        }
    })
});