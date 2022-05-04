AccountEditProfile = {};

(function (obj, $) {
    function initContainer() {
        let container = obj.container;
        let url = container.data('render-form-url');
        $.ajax({
            type: 'GET',
            url: url,
        }).done(function (response) {
            container.html(response.content);
            obj.form = container.find('form')[0];
            initWidgets();
            initFormActions();
        });
    }

    function initWidgets() {
        let container = obj.container;
        let phoneFields = container.find(".phone-number");
        phoneFields.inputmask("mask", {"mask": "+380(99)-999-9999"});
    }

    function initFormActions() {
        let $form = $(obj.form);

        $form.on('reset', function (e) {
            e.preventDefault();
            initContainer();
        })

        $form.on('submit', function (e) {
            e.preventDefault();
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: $form.serialize(),
                success: function (response) {
                    clearForm();
                    $('<div/>', {
                        'class': 'success-message alert alert-success',
                        'text': 'Profile info is saved'
                    }).prependTo($form);
                }, error: function (response) {
                    clearForm();
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
            })
        });
    }

    function clearForm() {
        let $form = $(obj.form);
        $form.find('.has-error').removeClass();
        $form.find('.error-message').remove();
        $form.find('.success-message').remove();
    }

    function init() {
        console.log('Load edit profile');
        obj.container = $('#profile-data-container');
        initContainer();
    }

    obj.init = init;
})(AccountEditProfile, $);


$(document).ready(function () {
    AccountEditProfile.init();
});
