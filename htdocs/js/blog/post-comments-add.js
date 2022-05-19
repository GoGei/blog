PostCommentAdd = {};
(function (obj, $) {
    function init() {
        $('.post-comment-save').click(function (e) {
            e.preventDefault();
            let $textInput = $('#comment-input')
            let text = $textInput.val();
            let $postContent = $('.post-view-content')
            let url = $postContent.data('post-add-comment');
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'text': text,
                }, success: function (response) {
                    $textInput.val(null);
                    addPostComment(response.id);
                }, error: function (response) {
                    handleErrors(response);
                }
            })
        })
    }

    function addPostComment(commentId) {
        let $commentContainer = $('.post-comments-section');
        $.ajax({
            url: $commentContainer.data('post-comment-render-url'),
            data: {'comment_id': commentId},
            success: function (response) {
                $commentContainer.append(response.content);
                reInitPostCommentActions();
            }
        })
    }

    function handleErrors(response) {
        let $form = $('#post-comment-form');
        $form.find('.error-message').remove();
        let errors = response.responseJSON;
        $.map(errors, function (messages, name) {
            let field = $form.find(`[name=${name}]`);
            if (field.length) {
                $.each(messages, function (i, message) {
                    $('<div/>', {
                        'class': 'error-message text-right text-danger',
                        'text': message
                    }).appendTo($form);
                });
            }
        });
    }

    obj.init = init;
})(PostCommentAdd, $);


$(document).ready(function () {
    PostCommentAdd.init();
});