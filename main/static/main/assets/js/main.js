function toggleSave(post_id) {
    $.ajax({
        url: "/save/" + post_id + "/",
        success: function(data) {
            $("#savePost" + post_id).html(data.img);
            $("#savePostdata" + post_id).html(data.p);
        },
        error: function(data) {
            $('#errors' + post_id).html(data.responseText);
        }
    });
};


function toggleLike(post_id) {
    $.ajax({
        url: "/like/" + post_id + "/",
        success: function(data) {
            $("#likeCount" + post_id).html(data.likes_count);
            $("#likePost" + post_id).html(data.img);
        }
    });
};


function toggleFollow(post_author) {
    $.ajax({
        url: "/follow/" + post_author + "/",
        success: function(data) {
            $("#followUser" + post_author).html(data.img);
        }
    });
};


function toggleUnfollow(follower_id) {
    $.ajax({
        url: "/unfollow/" + follower_id + "/",
        success: function(data) {
            $("#unfollow" + follower_id).html(data);
            $("#count" + follower_id).html(data.followings_count)
        }
    });
};