$(window).on("scroll", function() {
	var scrollHeight = $(document).height();
	var scrollPosition = $(window).height() + $(window).scrollTop();
	if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
	     console.log('near buttom!');
	}
});