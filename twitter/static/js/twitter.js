$(document).ready(function () {
    $('.follow').each(function(index,el){
        $(el).click(function(e){
            e.preventDefault()
            target = $(el).attr('data-target')
            follower = $(el).attr('data-follower')
            $.ajax({
                url:`follow/${target}/${follower}`,
                data:'',
                success:function(response){
                    if(response['is_followed']){
                        alert($(el).closest('.unfollow').css({'display':'block'}))
                        $(el).closest('.unfollow').css({'display':'block'})
                    }
                }
            })
        })
    })
    $('.unfollow').each(function(index,el){
        $(el).click(function(e){
            e.preventDefault()
            target = $(el).attr('data-target')
            follower = $(el).attr('data-follower')
            $.ajax({
                url:`unfollow/${target}/${follower}`,
                data:'',
                success:function(response){
                    if(response['is_unfollowed']){
                        location.reload();
                    }
                }
            })
        })
    })
});