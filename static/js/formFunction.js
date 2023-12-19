$(document).ready(function () {
    // jQuery code
    const createTradeForm = $('#createTradeForm');
    const showCreateTradeForm = $('#showCreateTradeForm');
    const hideCells = $('.hide-cell');
    const createTradeButton = $('#createTradeButton'); // Corrected selector


    // Add an event listener for the delete button
    $('.delete-trade-button').click(function () {
        const tradeId = $(this).data('trade-id');
        const rowNumber = $(this).data('row-number');
        deleteTrade(tradeId, rowNumber);
    });

    showCreateTradeForm.click(function () {
        createTradeForm.toggleClass('hidden-form');

        // Toggle the visibility of the hide-cell elements
        hideCells.toggleClass('hidden-cell');

        // Hide the "Create Trade" button
        createTradeButton.hide();
    });


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


function handleSaveResponse(data, tradeId) {
    // Handle the response from the server after saving
    if (data.success) {
        // You may update other UI elements as needed
        console.log('Trade successfully saved:', tradeId);

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


