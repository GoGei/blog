PostCommentsEdit = {};
(function (obj, $) {
    function clearForm(initialValue = null, mode='add') {
        let $form = $('#post-comment-form');
        $form.find('.error-message').remove();

        if (mode === 'add') {
            $('.post-comment-save').removeAttr('hidden');
            $('.post-comment-edit').attr('hidden', 'hidden');
            $('.post-comment-cancel').attr('hidden', 'hidden');
        } else {
            $('.post-comment-save').attr('hidden', 'hidden');
            $('.post-comment-edit').removeAttr('hidden');
            $('.post-comment-cancel').removeAttr('hidden');
        }

        let $textField = obj.input;
        $textField.val(initialValue);
    }

    function initButtons() {
        $('.post-comment-cancel').click(function (e) {
            e.preventDefault();
            clearForm();
        });
        $('.post-comment-edit').click(function (e) {
            e.preventDefault();
            let $textInput = $('#comment-input')
            let text = $textInput.val();
            $.ajax({
                type: 'PATCH',
                url: obj.actionUrl,
                data: {
                    'text': text,
                }, success: function (response) {
                    clearForm();
                    replacePostComment(response.id);
                }, error: function (response) {
                    handleErrors(response);
                }
            })
        });
    }

    function replacePostComment(commentId) {
        $.ajax({
            url: $('.post-comments-section').data('post-comment-render-url'),
            data: {'comment_id': commentId},
            success: function (response) {
                $(`#post-comment-container-${commentId}`).replaceWith(response.content);
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

    function init() {
        $('.post-comment-edit-button').unbind('click');
        $('.post-comment-edit-button').on('click', function (e) {
            e.preventDefault();
            let postCommentId = $(this).data('post-comment-id');
            let textContainer = $(`#post-comment-container-${postCommentId}`).find('.post-comment-text');
            let initialText = $.parseHTML(textContainer.html())[1].nodeValue;

            let $textField = $('#comment-input');
            obj.input = $textField;
            obj.actionUrl = $(this).data('action-url');
            $('html, body').animate({scrollTop: $textField.offset().top}, 500);
            clearForm(initialText, 'edit');
            initButtons();
        });
    }

    obj.init = init;
})(PostCommentsEdit, $)
