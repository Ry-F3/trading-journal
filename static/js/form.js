// Form Calculations
$(document).ready(function () {
    // jQuery code
    $('#id_leverage, #id_margin, #id_open_price, #id_current_price').on('input', function () {
        console.log('Input event triggered');
        calculateReturnPnl();
    });

    // Function to calculate return_pnl
    function calculateReturnPnl() {
        var leverage = parseFloat($('#id_leverage').val()) || 0;
        var margin = parseFloat($('#id_margin').val()) || 0;
        var openPrice = parseFloat($('#id_open_price').val()) || 0;
        var currentPrice = parseFloat($('#id_current_price').val()) || 0;

        // Check if all required numeric fields have values
        var allFieldsFilled = margin && openPrice && currentPrice;

        if (allFieldsFilled) {
            // Calculate percentage Change
            var percentageChange = ((currentPrice - openPrice) / openPrice) * leverage * 100;

            // Format percentageChange with two decimal places
            percentageChange = percentageChange.toFixed(2);

            // Log percentage Change
            console.log('Percentage Change:', percentageChange, '%');

            // Calculate Return PnL
            var returnPnl;

            if (percentageChange >= 0) {
                // Positive percentage Change, use the formula for positive returns
                returnPnl = (percentageChange / 100) * margin;
                // Update the return_pnl field
                $('#id_return_pnl').val(returnPnl.toFixed(2));
            } else {
                // Negative percentage Change, use the formula for negative returns
                returnPnl = (percentageChange / 100) * margin;
                returnPnlNegative = returnPnl;
                console.log(returnPnlNegative)
                // Update the return_pnl field
                $('#id_return_pnl').val(returnPnlNegative.toFixed(2));
            }



            console.log('Calculating return pnl');
            // Log relevant variables
            console.log('Margin:', margin);
            console.log('Open Price:', openPrice);
            console.log('Current Price:', currentPrice);
            console.log('Return PnL:', returnPnl.toFixed(2));
            console.log('Percentage Change:', percentageChange, '%');
        } else {
            console.log('Not all required numeric fields have values. Cannot calculate return pnl.');
            // Clear the return pnl field if input is incomplete
            $('#id_return_pnl').val('');
        }
    }

});


