DeletePostModalForm = {};

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
                let content = response.content;
                let $modalBody = obj.modal.find('.modal-content');
                $modalBody.html(content);
            }
        });
        initButtons();
    }

    function initButtons() {
        let $deleteButton = $('.form-delete-button');

        $deleteButton.on('click', function (e){
            e.preventDefault();
            let $form = $(obj.modal.find('form'));
            $.ajax({
                type: $form.data('method'),
                url: $form.attr('action'),
                data: {'post': obj.postId},
            }).done(function (){
                closeModal();
                $(`#post-id-${obj.postId}`).remove();
            });
        });
    }

    function init(postId){
        console.log('Load delete post modal');
        let $modal = $('#profileDeleteModal');
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
        return $modal
    }

    obj.init = init;
})(DeletePostModalForm, $);


$(document).on('click', '.delete-post', function (){
    let postId = $(this).data('post-id');
    let $modal = DeletePostModalForm.init(postId);
    $modal.modal('show');
})
