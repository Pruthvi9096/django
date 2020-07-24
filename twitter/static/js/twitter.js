$(document).ready(function () {
    $('.follow').each(function (index, el) {
        $(el).click(function (e) {
            e.preventDefault()
            target = $(el).attr('data-target')
            follower = $(el).attr('data-follower')
            $.ajax({
                url: `/follow/${target}/${follower}`,
                data: '',
                success: function (response) {
                    if (response['is_followed']) {
                        $(el).css({ 'display': 'none' })
                        $('#unfollow-' + target).css({ 'display': 'block' });
                    }
                }
            })
        })
    })
    $('.unfollow').each(function (index, el) {
        $(el).click(function (e) {
            e.preventDefault()
            target = $(el).attr('data-target')
            follower = $(el).attr('data-follower')
            $.ajax({
                url: `/unfollow/${target}/${follower}`,
                data: '',
                success: function (response) {
                    if (response['is_unfollowed']) {
                        $(el).css({ 'display': 'none' })
                        $('#follow-' + target).css({ 'display': 'block' });
                    }
                }
            })
        })
    })
    $('.reply').click(function (e) {
        e.preventDefault();
        var comment = this;
        var url = `/reply-to/${comment.id}/`
        $.ajax({
            url: url,
            data: '',
            success: function (response) {
                // $('#form').remove();
                $('#comments').find('#commentForm').remove();
                $(comment).after(response['form'])
                $(comment).hide();
                $('#commentForm').attr('action', url)
                $('#comment-id').val(comment.id)
            }
        })
    });
    $('.delete').click(function (e) {
        e.preventDefault();
        var comment = this;
        var id = $(comment).attr('data-target')
        alert("Are you sure delete this comment?");
        var url = `/delete-comment/${id}`;
        $.ajax({
            url: url,
            data: '',
            success: function (response) {
                if (response['deleted']) {
                    $(comment).closest('.comment-body').remove();
                    // alert("Comment Deleted Successfully!")
                }
            }
        })

    })
    $('#search').keyup(function (e) {
        var query = $(this).val()
        if (query !== '' && query !== null && query !== undefined) {
            $.ajax({
                url: '/search-profile/',
                data: { 'q': query },
                success: function (response) {
                    if (response['list']) {
                        $('#results').html(response['list'])
                    }
                    else {
                        $('#results').html('')
                    }
                }
            })
        }
        else {
            $('#results').html('')
        }
    });
    $('#followers').click(function(e){
        e.preventDefault();
        profileId = $('#followers').attr('data-profile')
        console.log(profileId)
        $.ajax({
            url:`/followers/${profileId}`,
            data:'',
            success: function(response) {
                if(response['followers']){
                    $('#feed-content').html(response['followers'])
                    $('#feed-title').text("Followers")
                }
            }
        })
    })
    $('#followings').click(function(e){
        e.preventDefault();
        profileId = $('#followings').attr('data-profile')
        console.log(profileId)
        $.ajax({
            url:`/followings/${profileId}`,
            data:'',
            success: function(response) {
                if(response['followings']){
                    $('#feed-content').html(response['followings'])
                    $('#feed-title').text("Followings")
                }
            }
        })
    })
    $('#posts').click(function(e){
        e.preventDefault();
        profileId = $('#posts').attr('data-profile')
        console.log(profileId)
        $.ajax({
            url:`/posts/${profileId}`,
            data:'',
            success: function(response) {
                if(response['posts']){
                    $('#feed-content').html(response['posts'])
                    $('#feed-title').text("Posts")
                }
            }
        })
    })
});
