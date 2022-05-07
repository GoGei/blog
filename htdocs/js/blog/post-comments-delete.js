PostCommentsDelete = {};
(function (obj, $) {
    function init() {
        $('.post-comment-delete-button').unbind('click');
        $('.post-comment-delete-button').on('click', function (e) {
            e.preventDefault();
            console.log('Post comment delete');
            let currentButton = $(this);
            $.ajax({
                type: 'DELETE',
                url: currentButton.data('action-url'),
            }).done(function () {
                let $postComment = currentButton.closest('.post-comment-container');
                $postComment.remove();
            })
        });
    }

    obj.init = init;
})(PostCommentsDelete, $)