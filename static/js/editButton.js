$(document).ready(function () {
    console.log('Script loaded');

    const createTradeForm = $('#createTradeForm');
    const hideCells = $('.hide-cell');  // Select hide-cell elements

    // Code for handling "Edit Trade" button click
    $(document).on('click', '.edit-trade-button', function () {
        // Display the form for editing
        try {
            const rowNumber = $(this).data('row-number');
            console.log(`Edit Trade clicked for row ${rowNumber}`);
            editTrade(rowNumber);
        } catch (error) {
            console.error('Error in edit-trade-button click event:', error);
        }
    });

    function editTrade(rowNumber) {
        if (rowNumber !== null) {
            console.log(`Attempting to fetch trade details for row: ${rowNumber}`);
            fetch(`/get_trade_details_by_row/${rowNumber}/`, {
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
                createTradeForm.find('#id_symbol').val(tradeDetails.symbol);
                createTradeForm.find('#id_date').val(tradeDetails.date);
                createTradeForm.find('#id_status').val(tradeDetails.status);
                createTradeForm.find('#id_long_short').val(tradeDetails.long_short);
                createTradeForm.find('#id_position').val(tradeDetails.position);
                createTradeForm.find('#id_margin').val(tradeDetails.margin);
                createTradeForm.find('#id_leverage').val(tradeDetails.leverage);
                createTradeForm.find('#id_open_price').val(tradeDetails.open_price);
                createTradeForm.find('#id_current_price').val(tradeDetails.current_price);
                createTradeForm.find('#id_return_pnl').val(tradeDetails.return_pnl);
    

                // Remove hide-cell class from td elements in the form
                hideCells.removeClass('hide-cell');

                // Display the form for editing
                createTradeForm.removeClass('hidden-form');

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

});
