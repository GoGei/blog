$(window).on("scroll", function() {
	var scrollHeight = $(document).height();
	var scrollPosition = $(window).height() + $(window).scrollTop();
	if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
	     console.log('near buttom!');
	}
});


function loadPosts() {
    let $postsContainer = $('#posts-container');
    let postsUrl = $postsContainer.data('posts-url');

	let filterData = {};
    let categoryId = '';
    if (categoryId){
    	filterData['category'] = categoryId;
	}
    $.ajax({
        type: 'GET',
        url: postsUrl,
        data: filterData,
        success: function (data) {
            console.log(data);
            $.map(data.results, function (post, i) {
                // console.log(post);
            })
        }
    })
}