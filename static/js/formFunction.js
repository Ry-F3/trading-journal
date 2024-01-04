console.log()
$(document).ready(function () {
    // jQuery code
    const createTradeForm = $('#createTradeForm');
    const showCreateTradeForm = $('#showCreateTradeForm');
    const hideCells = $('.hide-cell');
    const createTradeButton = $('#createTradeButton');
    const container = $('.scrollbar-container');


    let createTradeFormActive = false; // Flag to track if the createTrade form is active
    console.log('form inactive', createTradeFormActive);

    // Add an event listener for the delete button
    $('.delete-trade-button').click(function () {
        const tradeId = $(this).data('trade-id');
        const rowNumber = $(this).data('row-number');
        deleteTrade(tradeId, rowNumber);
    });


    // Add an event listener for pagination links
    $('.pagination a').on('click', function (e) {
        console.log('Pagination link clicked.');
        // Call the function to update row numbers and IDs
        updateRowNumbersAndIds();

        console.log('Content updated.');

    });


    showCreateTradeForm.click(function () {
        const buttonText = $(this).text();
        console.log('Current state of createTradeForm:', createTradeForm);

        if (buttonText === 'Create Trade') {
            createTradeForm.css('display', 'block');
            console.log('Current state of createTradeForm:', createTradeForm.css('display'));
            // Code for handling "Create Trade" button click
            createTradeFormActive = true;
            handleFormVisibility();
        } else if (buttonText === 'Cancel Trade') {
            createTradeForm.css('display', 'none');
            console.log('Current state of createTradeForm:', createTradeForm.css('display', 'none'));
            // Code for handling "Cancel Trade" button click
            console.log('editMode:', editMode);
            createTradeFormActive = false;
            handleFormVisibility();
        }
    });

    // Function to handle form visibility and behavior
    function handleFormVisibility() {
        console.log('inside function', createTradeFormActive);
        const wasFormActive = createTradeFormActive;
        console.log('edit in function', editMode);

        if (createTradeFormActive) {
            // Code for when the form is active
            console.log('Form is now active');
            container.scrollTop(container[0].scrollHeight);

            // Additional logic specific to form activation
            // ...
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

            // Toggle the visibility of the ID cell based on createTradeFormActive
            $('.id-cell').each(function () {
                if (createTradeFormActive) {
                    // If form is active, hide the ID cell
                    $(this).css('display', 'none');
                } else {
                    // If form is inactive, show the ID cell as table-cell
                    $(this).css('display', 'table-cell');
                }
            });

            // // Toggle the visibility of the hide-cell elements
            console.log('Before Toggle: Hide Cells Visibility 0:', hideCells.hasClass('hidden-cell'));
            hideCells.toggleClass('hidden-cell', createTradeFormActive);
            console.log('After Toggle: Hide Cells Visibility 0:', hideCells.hasClass('hidden-cell'));

            // Function to enable input fields
            function disableFields() {
                $('#id_position, #id_margin, #id_leverage, #id_open_price, #id_current_price, #id_return_pnl').prop('disabled', true);
            }

            console.log('Before enableFields()');
            disableFields();
            console.log('After enableFields()');

            // Check your condition here and set the save type accordingly
            if (createTradeFormActive) {
                $('#saveType').val('regular');

            } else {
                $('#saveType').val('overwrite');
            }


        } else {
            // Code for when the form is inactive
            console.log('Form is now inactive');
            container.scrollTop(0);


            // Clear the form fields
            $('#id_symbol, #id_date, #id_status, #id_long_short, #id_position, #id_margin, #id_leverage, #id_open_price, #id_current_price, #id_return_pnl').val('');

            // Toggle the visibility of the hide-cell elements
            console.log('Before Toggle: Hide Cells Visibility 1:', hideCells.hasClass('hidden-cell'));
            hideCells.toggleClass('hidden-cell', createTradeFormActive);
            console.log('After Toggle: Hide Cells Visibility 1:', hideCells.hasClass('hidden-cell'));

            // Toggle the visibility of the ID cell based on createTradeFormActive
            $('.id-cell').each(function () {
                if (createTradeFormActive) {
                    // If form is active, hide the ID cell
                    $(this).css('display', 'none');
                } else {
                    // If form is inactive, show the ID cell as table-cell
                    $(this).css('display', 'table-cell');
                }
            });

        }

        // Toggle the "save-button" class based on form activity
        $('#save').toggleClass('save-button', createTradeFormActive);
        $('#save').toggleClass('save-edit-button', !createTradeFormActive);

        // Set the save type based on form activity
        $('#saveType').val(createTradeFormActive ? 'regular' : 'overwrite');

        // Log the value of saveType
        console.log('Save Type:', $('#saveType').val());


        // Revert the button text based on form activity
        showCreateTradeForm.text(createTradeFormActive ? 'Cancel Trade' : 'Create Trade');
    }



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


