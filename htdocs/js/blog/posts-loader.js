$(document).ready(function () {
    loadPosts();
});


$(window).on("scroll", function () {
    let scrollHeight = $(document).height();
    let scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
        let nextPostsUrl = $('#posts-container').data('posts-next-url');
        loadPosts(nextPostsUrl);
    }
});


function loadPosts(requestUrl='') {
	let container = $('#posts-container');
	if (!requestUrl) {
		requestUrl = container.data('posts-url')
	}

	getData(function (data) {
		console.log('data', data);
		$.ajax({
			type: 'GET',
			url: requestUrl,
			data: data,
			success: function (posts) {
				container.data('posts-next-url', posts.next);
				$.map(posts.results, function (post) {
					console.log(post.id);
				})
			}
		});
	});
}


function getData(callback) {
	let data = {};

	let url = new URL(document.location.href);
	if (url.searchParams.has('category')) {
		let slug = url.searchParams.get('category');
		getIdOfCategoryBySlug(slug, function (categoryId) {
			data['category'] = categoryId;
			callback(data);
		});
	} else {
		callback(data);
	}
}
