$(document).ready(function () {
    // jQuery code
    const createTradeForm = $('#createTradeForm');
    const showCreateTradeForm = $('#showCreateTradeForm');
    const hideCells = $('.hide-cell');
    const createTradeButton = $('#createTradeButton'); // Corrected selector

    // Add an event listener for the delete button
    $('.delete-trade-button').click(function () {
        const tradeId = $(this).data('trade-id');
        deleteTrade(tradeId);
    });

    showCreateTradeForm.click(function () {
        createTradeForm.toggleClass('hidden-form');

        // Toggle the visibility of the hide-cell elements
        hideCells.toggleClass('hidden-cell');

        // Hide the "Create Trade" button
        createTradeButton.hide();
    });
});

function deleteTrade(tradeId) {
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
            handleDeleteResponse(data, tradeId);
        },
        error: function (error) {
            console.error('Error:', error);
        },
    });
}

function handleDeleteResponse(data, tradeId) {
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
        console.log('Trade successfully deleted:', tradeId);
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

// Helper function to update row numbers and IDs in the UI
function updateRowNumbersAndIds() {
    $('.trade-row').each(function (index) {
        const rowNumberElement = $(this).find('.row-number');
        if (rowNumberElement.length) {
            // Update row numbers to match trade IDs
            const newTradeId = $(this).data('trade-id');
            rowNumberElement.text(newTradeId);
        }

        // Update the trade ID and row ID based on the updated row_number
        const updatedTradeId = $(this).data('trade-id');
        const updatedRowId = `tradeRow${updatedTradeId}`;
        $(this).attr('id', updatedRowId);
    });
}

