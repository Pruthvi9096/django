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
                        $(el).css({'display':'none'})
                        $('#unfollow-'+target).css({'display':'block'});
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
                        $(el).css({'display':'none'})
                        $('#follow-'+target).css({'display':'block'});
                    }
                }
            })
        })
    })
});