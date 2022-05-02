$(".go-to-the-top").click(function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

$.ajaxSetup({
    headers: {"X-CSRFToken": $.cookie('csrftoken')}
});