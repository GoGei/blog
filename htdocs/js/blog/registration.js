RegistrationModalForm = {};

(function (obj, $) {
    function clearModal() {
        obj.modal.find('.modal-body').empty();
    }

    function closeModal() {
        obj.modal.modal('hide');
        clearModal();
    }

    function loadModal() {
        $.ajax({
            url: obj.modal.data('form-url'),
            async: false,
            success: function (response) {
                let form = response.form;
                console.log(form)
                let $modalBody = obj.modal.find('.modal-body');
                $modalBody.html(form);
            }
        });
        initWidgets();
        initButtons();
    }

    function initWidgets() {
        let phoneFields = obj.modal.find(".phone-number");
        phoneFields.inputmask("mask", {"mask": "+380(99)-999-9999"});
    }

    function initButtons() {
        let $saveButton = $('.form-save-button');

        $saveButton.on('click', function (e) {
            e.preventDefault();
            let $form = $(obj.modal.find('form'));
            let formData = $form.serialize();
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: formData,
            }).done(function (response) {
                if (response.success) {
                    $form[0].reset();
                    closeModal();
                    window.location.replace(response.redirect_url);
                } else {
                    $form.find('.error-message').remove();
                    $form.find('.has-error').removeClass('has-error');
                    let errors = response.errors;
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
    }

    function init() {
        console.log('Load register modal');
        let $modal = $('#registrationModal');
        obj.modal = $modal;
        $modal.on('hidden.bs.modal', function () {
            clearModal();
        });
        $modal.on('hide.bs.modal', function () {
            clearModal();
        });
        $modal.on('show.bs.modal', function () {
            loadModal();
        });
    }

    obj.init = init;
})(RegistrationModalForm, $);


$(document).ready(function () {
    RegistrationModalForm.init();
});
