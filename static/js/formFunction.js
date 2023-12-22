console.log()
$(document).ready(function () {
    // jQuery code
    const createTradeForm = $('#createTradeForm');
    const showCreateTradeForm = $('#showCreateTradeForm');
    const hideCells = $('.hide-cell');
    const createTradeButton = $('#createTradeButton');
    const container = $('.scrollbar-container');


    let createTradeFormActive = false; // Flag to track if the createTrade form is active
    console.log(createTradeFormActive);

    // Add an event listener for the delete button
    $('.delete-trade-button').click(function () {
        const tradeId = $(this).data('trade-id');
        const rowNumber = $(this).data('row-number');
        deleteTrade(tradeId, rowNumber);
    });


    showCreateTradeForm.click(function () {
        createTradeFormActive = !createTradeFormActive; // Toggle the flag
        console.log(createTradeFormActive);
        createTradeForm.toggleClass('hidden-form');

        console.log('scroll:', container);

        // Scroll to the bottom of the container
        container.scrollTop(container[0].scrollHeight);

        // Additional log to check if the code reaches this point
        console.log('Scrolled to the bottom');

        // Clear the form fields for regular edit
        $('#id_symbol').val('');
        $('#id_date').val('');
        $('#id_status').val('');
        $('#id_long_short').val('');
        $('#id_position').val('');
        $('#id_margin').val('');
        $('#id_leverage').val('');
        $('#id_open_price').val('');
        $('#id_current_price').val('');
        $('#id_return_pnl').val('');

        // Toggle the visibility of the hide-cell elements
        hideCells.toggleClass('hidden-cell');

        // Hide the "Create Trade" button
        createTradeButton.hide();


        // Function to enable input fields
        function disableFields() {
            $('#id_position, #id_margin, #id_leverage, #id_open_price, #id_current_price, #id_return_pnl').prop('disabled', true);
        }

        console.log('Before enableFields()');
        disableFields();
        console.log('After enableFields()');

        // Add or remove the 'save-button' class to the td element based on createTradeFormActive
        $('#save').toggleClass('save-button', createTradeFormActive);
        $('#save').removeClass('save-edit-button', createTradeFormActive);

        // Check your condition here and set the save type accordingly
        if (createTradeFormActive) {
            $('#saveType').val('regular');

        } else {
            $('#saveType').val('overwrite');
        }

        // Log the value of saveType
        console.log('Save Type:', $('#saveType').val());

    });


    // Function to handle the deletion of a trade
    function deleteTrade(tradeId, rowNumber, callback) {
        // Get the CSRF token from the page
        const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        // Using $.ajax to send a DELETE request to the server
        $.ajax({
            url: `/delete-trade/${tradeId}/`,
            type: 'DELETE',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            xhrFields: {
                withCredentials: true, // Include credentials (e.g., cookies) in the request
            },
            success: function (data) {
                handleDeleteResponse(data, tradeId, rowNumber);
                if (callback) {
                    // Call the callback function if provided
                    callback();
                }
            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    }

    // Add an event listener for the delete button
    $('.delete-trade-button').click(function () {
        const tradeId = $(this).data('trade-id');
        const rowNumber = $(this).data('row-number');

        // Call deleteTrade and pass a callback function to reload the page
        deleteTrade(tradeId, rowNumber, function () {
            // Reload the page
            window.location.reload();
        });
    });

    function handleDeleteResponse(data, tradeId, rowNumber) {
        const rowId = `tradeRow${tradeId}`;

        // Handle the response from the server
        if (data.success) {
            // If the deletion was successful, remove the row from the UI
            const row = $(`#${rowId}`);
            if (row.length) {
                row.remove();
            }

            // Update row numbers and IDs in the UI after deletion
            updateRowNumbersAndIds();

            // Add a message or log to indicate success
            console.log(`Trade successfully deleted: Trade ID - ${tradeId}, Row Number - ${rowNumber}`);
        } else {
            // Handle errors or provide feedback to the user
            console.error('Deletion failed:', data.error);
        }
    }


});



function handleSaveResponse(data, tradeId) {
    // Handle the response from the server after saving
    if (data.success) {
        // You may update other UI elements as needed
        console.log('Trade successfully saved:', tradeId);
        createTradeFormActive = false;

        // Update row numbers and IDs in the UI after saving
        updateRowNumbersAndIds();
    } else {
        // Handle errors or provide feedback to the user
        console.error('Save failed:', data.error);
    }
}


function updateRowNumbersAndIds() {
    // Code to update row numbers and IDs in the UI
    // For example, you can iterate through rows and update their IDs and data attributes
    $('.delete-trade-button').each(function (index) {
        const tradeId = $(this).data('trade-id');
        $(this).data('row-number', index + 1);
        $(this).closest('tr').attr('id', `tradeRow${tradeId}`);
    });
}


