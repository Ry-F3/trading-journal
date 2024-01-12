$(document).ready(function () {

    const createTradeForm = $('#createTradeForm');
    const hideCells = $('.hide-cell');  // Select hide-cell elements
    let editMode = false;  // Flag to track if the user is in edit mode
    let currentRowNumber;  // Variable to store the current row number in edit mode
    let currentTradeId;
    const container = $('.scrollbar-container');

    // Code for handling "Edit Trade" button click
    $(document).on('click', '.edit-trade-button', function () {
        // Display the form for editing
        try {
            const tradeId = $(this).data('trade-id');
            const rowNumber = $(this).data('row-number');
            editTrade(tradeId, rowNumber);
        } catch (error) {
            console.error('Error in edit-trade-button click event:', error);
        }

        // Scroll to the bottom of the container
        container.scrollTop(container[0].scrollHeight);

    });


    // Code for handling "Save Trade" button click
    $(document).on('click', '#save-button', function () {
        // Check if the user is in edit mode
        if (editMode) {
            saveEditedTrade();
        } 
    });

    function editTrade(tradeId, rowNumber) {
        if (rowNumber !== null) {
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
                    if (data.success) {
                        editMode = true;
                        currentTradeId = tradeId;
                        currentRowNumber = rowNumber;
                        // Add or update hidden input fields for current_trade_id and current_row_number
                        addOrUpdateHiddenInput('currentTradeId', 'current_trade_id', currentTradeId);
                        addOrUpdateHiddenInput('currentRowNumber', 'current_row_number', currentRowNumber);
                        $('#showCreateTradeForm').text('Create Trade');

                        $('#save').toggleClass('save-edit-button', editMode);
                        $('#save').removeClass('save-button', editMode);

                        if (editMode) {
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

                // Update global variables based on the value of long_short
                if (tradeDetails.long_short === 'long') {
                    isShortSelected = false;
                    isLongSelected = true;
                } else if (tradeDetails.long_short === 'short') {
                    isShortSelected = true;
                    isLongSelected = false;
                }

                // Toggle the visibility of the ID cell based on createTradeFormActive
                $('.id-cell').each(function () {
                    if (editMode) {
                        // If form is active, hide the ID cell
                        $(this).css('display', 'none');
                    } else {
                        // If form is inactive, show the ID cell as table-cell
                        $(this).css('display', 'table-cell');
                    }
                });

                // Function expression to enable input fields
                var enableFields = function() {
                    $('#id_symbol, #id_date, #id_status, #id_long_short, #id_position, #id_margin, #id_leverage, #id_open_price, #id_current_price, #id_return_pnl').prop('disabled', false);
                };

                enableFields();

                // Toggle the 'hide-cell' class on td elements in the form
                hideCells.toggleClass('hidden-cell', true);

                // Toggle the 'hidden-form' class on the createTradeForm
                createTradeForm.toggleClass('hidden-form', true);

                // Set the values of the hidden fields for overwrite
                $('#currentTradeId').val(currentTradeId);
                $('#currentRowNumber').val(currentRowNumber);

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
        $('#id_tatus').val(editedTradeData.status);
        $('#id_long_short').val(editedTradeData.long_short);
        $('#id_position').val(editedTradeData.position);
        $('#id_margin').val(editedTradeData.margin);
        $('#id_leverage').val(editedTradeData.leverage);
        $('#id_open_price').val(editedTradeData.open_price);
        $('#id_current_price').val(editedTradeData.current_price);
        $('#id_return_pnl').val(editedTradeData.return_pnl);
    }


});
