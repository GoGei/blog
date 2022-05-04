AccountGetProfile = {};

(function (obj, $) {
    function initContainer() {
        let container = obj.container;
        let url = container.data('profile-data-url');
        $.ajax({
            type: 'GET',
            url: url,
        }).done(function (response) {
            let htmlContent = '<li class="list-group-item text-muted">Activity <i class="fa fa-dashboard fa-1x"></i></li>'
            htmlContent += `<li class="list-group-item"><span class="pull-left"><strong>You liked</strong></span> ${response.likes_counter}</li>`
            htmlContent += `<li class="list-group-item"><span class="pull-left"><strong>Your posts</strong></span> ${response.posts_counter}</li>`
            htmlContent += `<li class="list-group-item"><span class="pull-left"><strong>Your comments</strong></span> ${response.comments__counter}</li>`
            container.html(htmlContent);
        });
    }

    function init() {
        console.log('Load profile data');
        obj.container = $('#profile-data-container');
        initContainer();
    }

    obj.init = init;
})(AccountGetProfile, $);


$(document).ready(function () {
    AccountGetProfile.init();
});
