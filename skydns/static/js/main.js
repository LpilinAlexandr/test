function show_errors($form, errors_json) {
    for (var name in errors_json) {
        for (var i in errors_json[name]) {
            var element = $form.find('[name="'+ name + '"]');
            var $parent_element = element.closest('div');
            $parent_element.append('<p style="margin-top: 5px; color: red;">'+ errors_json[name][i].message +'</p>');
        }
    }
    setTimeout(remove_errors, 2500, $form);
}

function remove_errors($form) {
    var $exist_error_tags = $form.find('p');
    $exist_error_tags.remove();
}

$(function () {
    $('#emailForm').on('submit', function (e) {
        var $self = $(this);
        e.preventDefault();
        $.post({
            url: $self.attr('action'),
            data: $self.serialize(),
            success: (function (result) {
               alert(result)
            }),
        }).fail(function (result) {
            var bad_result = result.responseText;
            var json_bad_result = JSON.parse(bad_result);
            show_errors($self, json_bad_result);
        });
    })
})