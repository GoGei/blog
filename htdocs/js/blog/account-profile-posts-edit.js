EditPostModalForm = {};

(function (obj, $) {
    function clearModal() {
        obj.modal.find('.modal-content').empty();
    }

    function closeModal(){
        obj.modal.modal('hide');
        clearModal();
    }

    function loadModal() {
        $.ajax({
            url: obj.modal.data('form-url'),
            async: false,
            data: {'post': obj.postId},
            success: function (response) {
                let form = response.form;
                let $modalBody = obj.modal.find('.modal-content');
                $modalBody.html(form);
            }
        });
        initButtons();
    }

    function initButtons() {
        let $saveButton = $('.form-save-button');
        let $cancelButton = $('.form-cancel-button');

        $saveButton.on('click', function (e){
            e.preventDefault();
            let $form = $(obj.modal.find('form'));
            let formData = $form.serialize();
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: formData,
                success: function (response) {
                    rerenderPost(response.id)
                    $form[0].reset();
                    closeModal();
                },
                error: function (response) {
                    $form.find('.error-message').remove();
                    $form.find('.has-error').removeClass('has-error');
                    let errors = response.responseJSON;
                    $.each(errors, function (name, messages) {
                        let field = $form.find(`[name=${name}]`);
                        if (field.length) {
                            let row = field.closest('.form-group');
                            row.addClass('has-error');
                            $.each(messages, function (i, message) {
                                $('<div/>', {
                                    'class': 'error-message text-right text-danger',
                                    'text': message
                                }).appendTo(row);
                            });
                        } else {
                            $.each(messages, function (i, message) {
                                $('<div/>', {
                                    'class': 'error-message alert alert-warning',
                                    'text': message
                                }).prependTo($form);
                            });
                        }
                    });
                }
            });
        });

        $cancelButton.on('click', function (e) {
            e.preventDefault();
            closeModal();
        })
    }

    function rerenderPost(objId){
        $.ajax({
            url: obj.modal.data('render-post-url'),
            data: {'post_id': objId},
            success: function (response){
                $(`#post-id-${objId}`).replaceWith(response.content);
            }
        })
    }

    function init(postId){
        console.log('Load edit post modal');
        let $modal = $('#profileEditModal');
        obj.modal = $modal;
        obj.postId = postId;
        $modal.on('hidden.bs.modal', function () {
            clearModal();
        });
        $modal.on('hide.bs.modal', function () {
            clearModal();
        });
        $modal.on('show.bs.modal', function () {
            loadModal();
        });
        return $modal;
    }

    obj.init = init;
})(EditPostModalForm, $);


$(document).on('click', '.edit-post', function (){
    let postId = $(this).data('post-id');
    let $modal = EditPostModalForm.init(postId);
    $modal.modal('show');
})
