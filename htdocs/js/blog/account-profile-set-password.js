AccountSetPassword = {};

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
        $(document).on('click', '.password-icon', function () {
            let input = $(this).parent().find('input');
            input.attr('type') === 'password' ? input.attr('type', 'text') : input.attr('type', 'password')
        });
    }

    function initFormActions() {
        let $form = $(obj.form);

        $form.on('submit', function (e) {
            e.preventDefault();
            $.ajax({
                type: $form.attr('method'),
                url: $form.attr('action'),
                data: $form.serialize(),
                success: function (response) {
                    window.location = $form.data("redirect-view");
                }, error: function (response) {
                    let errors = response.responseJSON;
                    $form.find('.error-message').remove();
                    $form.find('.has-error').removeClass('has-error');
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

    function init() {
        console.log('Load set password');
        obj.container = $('#profile-set-password-container');
        initContainer();
    }

    obj.init = init;
})(AccountSetPassword, $);
