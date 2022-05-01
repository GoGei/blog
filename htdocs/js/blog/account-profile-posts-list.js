$(document).ready(function () {
    loadPosts();
});


$(window).on("scroll", function () {
    let scrollHeight = $(document).height();
    let scrollPosition = $(window).height() + $(window).scrollTop();
    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
        let nextPostsUrl = $('#account-posts').data('posts-next-url');
        loadPosts(nextPostsUrl);
    }
});


function loadPosts(requestUrl='') {
	console.log('Load posts account');

	let container = $('#account-posts');
	if (!requestUrl) {
		requestUrl = container.data('account-posts-url')
	}

	$.ajax({
		type: 'GET',
		url: requestUrl,
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