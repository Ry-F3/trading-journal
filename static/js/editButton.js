$(document).ready(function () {
    console.log('Script loaded');

    const createTradeForm = $('#createTradeForm');
    const hideCells = $('.hide-cell');  // Select hide-cell elements
    let editMode = false;  // Flag to track if the user is in edit mode
    let currentRowNumber;  // Variable to store the current row number in edit mode
    let currentTradeId;

    // Code for handling "Edit Trade" button click
    $(document).on('click', '.edit-trade-button', function () {
        // Display the form for editing
        try {
            const tradeId = $(this).data('trade-id');
            const rowNumber = $(this).data('row-number');
            console.log(`Edit Trade clicked for row ${rowNumber}`);
            editTrade(tradeId, rowNumber);
        } catch (error) {
            console.error('Error in edit-trade-button click event:', error);
        }


    });

    // Code for handling "Save Trade" button click
    $(document).on('click', '#save-button', function () {
        // Check if the user is in edit mode
        if (editMode) {
            saveEditedTrade();
        } else {
            saveNewTrade();
        }
    });

    function editTrade(tradeId, rowNumber) {
        if (rowNumber !== null) {
            console.log(`Attempting to fetch trade details for row: ${rowNumber}`);
            fetch(`/get_trade_details/${tradeId}/${rowNumber}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Server response:', data);
                    if (data.success) {
                        editMode = true;
                        console.log("Edit mode:", editMode);
                        currentTradeId = tradeId;
                        currentRowNumber = rowNumber;
                        console.log('ID:', currentTradeId, "Row:", currentRowNumber);
                        // Add or update hidden input fields for current_trade_id and current_row_number
                        addOrUpdateHiddenInput('currentTradeId', 'current_trade_id', currentTradeId);
                        addOrUpdateHiddenInput('currentRowNumber', 'current_row_number', currentRowNumber);

                        $('#save').toggleClass('save-edit-button', editMode);
                        $('#save').removeClass('save-button', editMode);

                        if (editMode = true) {
                            $('#saveType').val('overwrite');
                        } else {
                            $('#saveType').val('regular');
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
                        }

                        // Log the value of saveType
                        console.log('Save Type:', $('#saveType').val());

                        console.log('Trade Id:', tradeId, 'Row:', currentRowNumber)
                        // Pass the edited data to the saveEditedTrade function
                        saveEditedTrade(data.trade_details);
                        handleEditResponse(data, rowNumber);
                    } else {
                        console.error('Error fetching trade details:', data.error);
                    }
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        }
    }

    function handleEditResponse(data, rowNumber) {
        const editedRow = $(`#tradeRow${rowNumber}`);
        if (editedRow.length) {
            if (data.success && data.trade_details) {
                // Populate the form fields with the fetched trade details
                const tradeDetails = data.trade_details;
                $('#id_symbol').val(tradeDetails.symbol);
                $('#id_date').val(tradeDetails.date);
                $('#id_status').val(tradeDetails.status);
                $('#id_long_short').val(tradeDetails.long_short);
                $('#id_position').val(tradeDetails.position);
                $('#id_margin').val(tradeDetails.margin);
                $('#id_leverage').val(tradeDetails.leverage);
                $('#id_open_price').val(tradeDetails.open_price);
                $('#id_current_price').val(tradeDetails.current_price);
                $('#id_return_pnl').val(tradeDetails.return_pnl);


                // Remove hide-cell class from td elements in the form
                hideCells.removeClass('hide-cell');

                // Display the form for editing
                createTradeForm.removeClass('hidden-form');

                console.log('Form:', createTradeForm);

                // Set the values of the hidden fields for overwrite
                $('#currentTradeId').val(currentTradeId);
                $('#currentRowNumber').val(currentRowNumber);

                // Log success
                console.log('Trade details loaded:', data.trade_details);
            } else {
                // Handle errors or provide feedback to the user
                console.error('Edit failed:', data.error);
            }
        } else {
            console.error('Edited row not found in the DOM:', `tradeRow${rowNumber}`);
        }
    }

    // Function to add or update a hidden input field
    function addOrUpdateHiddenInput(id, name, value) {
        let inputField = $(`#${id}`);
        if (inputField.length) {
            // Update existing input field
            inputField.val(value);
        } else {
            // Add new input field
            $('<input>').attr({
                type: 'hidden',
                id: id,
                name: name,
                value: value
            }).appendTo('form');
        }
    }

    // Function to save edited trade
    function saveEditedTrade(editedTradeData) {
        // Set the edited trade data in the form fields
        $('#id_symbol').val(editedTradeData.symbol);
        $('#id_date').val(editedTradeData.date);
        $('#sid_tatus').val(editedTradeData.status);
        $('#id_long_short').val(editedTradeData.long_short);
        $('#id_position').val(editedTradeData.position);
        $('#id_margin').val(editedTradeData.margin);
        $('#id_leverage').val(editedTradeData.leverage);
        $('#id_open_price').val(editedTradeData.open_price);
        $('#id_current_price').val(editedTradeData.current_price);
        $('#id_return_pnl').val(editedTradeData.return_pnl);
    }


});
