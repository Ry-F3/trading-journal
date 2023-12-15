$(document).ready(function () {
    // jQuery code
    $('#id_leverage, #id_margin, #id_open_price, #id_current_price').on('input', function () {
        console.log('Input event triggered');
        calculateReturnPnl();
    });

    // Function to calculate return_pnl
    function calculateReturnPnl() {
        // calculation logic goes here
        var leverage = parseFloat($('#id_leverage').val()) || 0;
        var margin = parseFloat($('#id_margin').val()) || 0;
        var originalMargin = parseFloat($('#id_margin').val()) || 0;
        var openPrice = parseFloat($('#id_open_price').val()) || 0;
        var currentPrice = parseFloat($('#id_current_price').val()) || 0;

        // Check if all required numeric fields have values
        var allFieldsFilled = leverage && margin && openPrice && currentPrice;

        var leverageMultiplier_result;
        

        if (allFieldsFilled) {
            // Calculate the return_pnl value
            if (leverage > 1) {
                leverageMultiplier = margin * leverage;
                leverageMultiplier_result = leverageMultiplier -  originalMargin;
                console.log(leverageMultiplier_result)
            } else if (leverage = 1) {
                leverageMultiplier = margin * leverage;
                leverageMultiplier_result = leverageMultiplier;  // Set the result here as well
                console.log(leverageMultiplier_result)
            } 

            margin = leverageMultiplier_result
            var stock = margin / openPrice;
            var returnPnl = (currentPrice - openPrice) * stock;

            // Format returnPnl with two decimal places
            margin = margin.toFixed(2);
            openPrice = openPrice.toFixed(2);
            currentPrice = currentPrice.toFixed(2);
            returnPnl = returnPnl.toFixed(2);

            // Update the return_pnl field
            $('#id_return_pnl').val(returnPnl);

            console.log('Calculating return pnl');
            // Log relevant variables
            console.log('Leverage:', leverage);
            console.log('Margin:', margin);
            console.log('Open Price:', openPrice);
            console.log('Current Price:', currentPrice);
            console.log('Return PnL:', returnPnl);
        } else {
            console.log('Not all required numeric fields have values. Cannot calculate return pnl.');
            // Clear the return pnl field if input is incomplete
            $('#id_return_pnl').val('');
        }
    }
});
