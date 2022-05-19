LoadPosts = {};
(function (obj, $) {
    $(window).on("scroll", function () {
        let scrollHeight = $(document).height();
        let scrollPosition = $(window).height() + $(window).scrollTop();
        if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
            let nextPostsUrl = $('#posts-container').data('posts-next-url');
            loadPosts(nextPostsUrl, false, false);
        }
    });

    $('#posts-search').on('keypress', function (e) {
        if (e.which == 13) {
            let value = this.value;
            let url = new URL(document.location.href);
            url.searchParams.set('search', value);
            window.history.pushState(null, '', url.toString());

            loadPosts('', true, true);
        }
    });

    function loadPosts(requestUrl = '', clearContainer = false, allowedGetFromBaseUrl=true) {
        console.log('Load posts');

        let container = $('#posts-container');
        if ((!requestUrl) && (allowedGetFromBaseUrl)) {
            requestUrl = container.data('posts-url')
        }

        if (clearContainer) {
            container.empty();
        }

        let data = getData();

        if (requestUrl) {
            $.ajax({
                type: 'GET',
                url: requestUrl,
                data: data,
                success: function (posts) {
                    container.data('posts-next-url', posts.next);
                    let postsData = JSON.stringify(posts.results);
                    let url = container.data('posts-render-url');
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

    function getData() {
        let data = {
            'limit': 10,
            'is_active': true,
            // 'category_is_active': true,
        };

        let url = new URL(document.location.href);
        if (url.searchParams.has('category')) {
            let slug = url.searchParams.get('category');
            data['category'] = getIdOfCategoryBySlug(slug);
        }

        if (url.searchParams.has('search')) {
            data['search'] = url.searchParams.get('search');
        }

        return data;
    }

    function loadInitPostSearch(){
        let url = new URL(document.location.href);
        if (url.searchParams.has('search')){
            $('#posts-search').val(url.searchParams.get('search'));
        }
    }

    function init() {
        loadPosts();
        loadInitPostSearch();
    }

    obj.init = init;

})(LoadPosts, $)

$(document).ready(function () {
    LoadPosts.init();
});