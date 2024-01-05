$(document).ready(function () {
    // Attach a click event to the like button
    $('.like-button').click(function (event) {
        // Prevent the default form submission behavior
        event.preventDefault();

        var object_id = $(this).closest('.like-form').find('input[name="object_id"]').val();

        // Use AJAX to send a POST request to the like_toggle view
        $.ajax({
            type: 'POST',
            url: '/like_toggle/',
            data: {
                'object_id': object_id,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            dataType: 'json',
            success: function (data) {
                // Update the like count on the page without reloading
                $('.like-count[data-object-id="' + object_id + '"]').text(data.like_count);
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});