PostCommentsList = {};

(function (obj, $) {
    $(window).on("scroll", function () {
        let scrollHeight = $(document).height();
        let scrollPosition = $(window).height() + $(window).scrollTop();
        if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
            let nextPostsUrl = obj.container.data('post-comments-next-url');
            loadPostComments(nextPostsUrl, false);
        }
    });

    function loadPostComments(requestUrl = '', allowedGetFromBaseUrl=true) {
        let container = obj.container;
        if ((!requestUrl) && (allowedGetFromBaseUrl)) {
            requestUrl = container.data('post-comments-load-url')
        }

        if (requestUrl) {
            $.ajax({
                type: 'GET',
                url: requestUrl,
                success: function (comments) {
                    container.data('post-comments-next-url', comments.next);
                    let commentsData = JSON.stringify(comments.results);
                    let url = container.data('post-comments-render-url');
                    $.ajax({
                        type: 'GET',
                        url: url,
                        data: {'comments': commentsData},
                        success: function (result) {
                            container.append(result.content);
                            reInitPostCommentActions();
                        }
                    })
                }
            });
        }
    }

    function init() {
        console.log('Load post comments');
        obj.container = $('.post-comments-section');
        loadPostComments();
    }

    obj.init = init;
})(PostCommentsList, $);


$(document).ready(function () {
    PostCommentsList.init();
});

function reInitPostCommentActions(){
    PostCommentsEdit.init();
    PostCommentsDelete.init();
    initCommentsLikesFunctionality();
}
