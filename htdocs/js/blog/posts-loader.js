LoadPosts = {};
(function (obj, $) {
    $(window).on("scroll", function () {
        let scrollHeight = $(document).height();
        let scrollPosition = $(window).height() + $(window).scrollTop();
        if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
            let nextPostsUrl = $('#posts-container').data('posts-next-url');
            loadPosts(nextPostsUrl);
        }
    });

    $('#posts-search').on('keypress', function (e) {
        if (e.which == 13) {
            let value = this.value;
            let url = new URL(document.location.href);
            url.searchParams.set('search', value);
            window.history.pushState(null, '', url.toString());

            loadPosts('', true);
        }
    });

    function loadPosts(requestUrl = '', clearContainer = false) {
        console.log('Load posts');

        let container = $('#posts-container');
        if (!requestUrl) {
            requestUrl = container.data('posts-url')
        }

        if (clearContainer) {
            container.empty();
        }

        let data = getData();

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

    function getData() {
        let data = {'limit': 10};

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

    function init() {
        loadPosts();
    }

    obj.init = init;

})(LoadPosts, $)

$(document).ready(function () {
    LoadPosts.init();
});