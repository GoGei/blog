$('.btn-like').on('click', function () {
    let $current = $(this);
    let $opposite = $('.btn-dislike');
    let dislikeClass = 'text-danger';
    let likeClass = 'text-success';

    if ($current.hasClass(likeClass)) {
        deactivateLikeElement($current, likeClass);
        $.get(getPostLikeUrl($current, 'deactivate'));
    } else {
        activateLikeElement($current, likeClass);
        $.get(getPostLikeUrl($current, 'like'));
    }

    if ($opposite.hasClass(dislikeClass)) {
        deactivateLikeElement($opposite, dislikeClass);
    }
});


$('.btn-dislike').on('click', function () {
    let $current = $(this);
    let $opposite = $('.btn-like');
    let dislikeClass = 'text-danger';
    let likeClass = 'text-success';

    if ($current.hasClass(dislikeClass)) {
        deactivateLikeElement($current, dislikeClass);
        $.get(getPostLikeUrl($current, 'deactivate'));
    } else {
        activateLikeElement($current, dislikeClass);
        $.get(getPostLikeUrl($current, 'dislike'));
    }

    if ($opposite.hasClass(likeClass)) {
        deactivateLikeElement($opposite, likeClass);
    }
});


function activateLikeElement($elem, activityClass) {
    let $label = $($elem.find('.like-label-counter')[0]);
    $label.html(parseInt($label.html(), 10) + 1);
    $elem.addClass(activityClass);
}


function deactivateLikeElement($elem, activityClass) {
    let $label = $($elem.find('.like-label-counter')[0]);
    $label.html(parseInt($label.html(), 10) - 1);
    $elem.removeClass(activityClass);
}


function getPostLikeUrl($current, activityName){
    let objId = $current.data('post-id');
    let host = $(location).attr('host');
    let protocol = $(location).attr('protocol');
    let url = `${protocol}//api.${host}/v1/posts/${objId}/${activityName}/`;
    console.log(url);
    return url;
}


function getPostCommentLikeUrl($current, activityName){
    let objId = $current.data('comment-id');
    let host = $(location).attr('host');
    let protocol = $(location).attr('protocol');
    let url = `${protocol}//api.${host}/v1/comments/${objId}/${activityName}/`;
    console.log(url);
    return url;
}



function initCommentsLikesFunctionality() {
    $('.btn-comment-like').unbind('click');
    $('.btn-comment-like').on('click', function () {
        let $current = $(this);
        let likeClass = 'text-success';

        if ($current.hasClass(likeClass)) {
            $current.removeClass(likeClass);
            $.get(getPostCommentLikeUrl($current, 'deactivate'));
        } else {
            $current.addClass(likeClass);
            $.get(getPostCommentLikeUrl($current, 'like'));
        }
    });
}