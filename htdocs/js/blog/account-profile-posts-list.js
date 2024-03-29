AccountLoadPosts = {};
(function (obj, $) {

    $(window).on("scroll", function () {
        let scrollHeight = $(document).height();
        let scrollPosition = $(window).height() + $(window).scrollTop();
        if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
            let nextPostsUrl = $('#account-posts').data('posts-next-url');
            loadPosts(nextPostsUrl, false);
        }
    });

    function loadPosts(requestUrl = '', allowedGetFromBaseUrl = true) {
        let container = $('#account-posts');
        if ((!requestUrl) && (allowedGetFromBaseUrl)) {
            requestUrl = container.data('account-posts-url')
        }

        if (requestUrl) {
            console.log('Load posts account');
            $.ajax({
                type: 'GET',
                url: requestUrl,
                data: {'limit': 10},
                success: function (posts) {
                    container.data('posts-next-url', posts.next);
                    let postsData = JSON.stringify(posts.results);
                    let url = container.data('account-posts-render-url');
                    $.ajax({
                        type: 'GET',
                        url: url,
                        data: {'posts': postsData},
                        success: function (result) {
                            container.append(result.content);
                        }
                    })
                }
            });
        }
    }

    function init() {
        loadPosts();
    }

    obj.init = init;

})(AccountLoadPosts, $)

$(document).ready(function () {
    AccountLoadPosts.init();
});