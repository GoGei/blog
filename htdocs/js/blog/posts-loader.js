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


function loadPosts(requestUrl='', clearContainer=false) {
	let container = $('#posts-container');
	if (!requestUrl) {
		requestUrl = container.data('posts-url')
	}

	if (clearContainer){
		container.empty();
	}

	getData(function (data) {
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
