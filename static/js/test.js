showCreateTradeForm.click(function () {
    const buttonText = $(this).text();

    if (buttonText === 'Create Trade') {
        // Check if the form is currently active
        const wasFormActive = createTradeFormActive;
        createTradeFormActive = !createTradeFormActive; // Toggle the flag
        console.log('form active', createTradeFormActive);
        createTradeForm.css('display', '');

        console.log('scroll:', container);

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
        hideCells.css('display', '');

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

        if (!createTradeFormActive && wasFormActive) {
            console.log('Form was toggled off');
            // Add your additional logic here
            container.scrollTop(0);
        } else {
            console.log("Form is Active");
        }


    } else if (buttonText === 'Cancel Trade') {
        // Code to handle "Cancel Trade" button click when form is active
        console.log('Cancel Trade clicked');

        // Toggle the visibility of the hide-cell elements
        hideCells.css('display', 'none');
        
        // Clear the form fields
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

        // Revert the button text back to "Create Trade"
        $(this).text('Create Trade');

        // Set the form as inactive
        createTradeFormActive = false;
        console.log('Form is now inactive');
        container.scrollTop(0);

        // Return here to exit the function and prevent further code execution
        return;
    }

});