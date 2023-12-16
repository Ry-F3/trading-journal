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
            // Calculate percentage increase
            var percentageIncrease = ((currentPrice - openPrice) / openPrice) * leverage * 100;

            // Format percentageIncrease with two decimal places
            percentageIncrease = percentageIncrease.toFixed(2);

            // Log percentage increase
            console.log('Percentage Increase:', percentageIncrease, '%');

            // Calculate Return PnL
            var returnPnl = (percentageIncrease / 100) * margin;

            // Update the return_pnl field
            $('#id_return_pnl').val(returnPnl.toFixed(2));

            console.log('Calculating return pnl');
            // Log relevant variables
            console.log('Margin:', margin);
            console.log('Open Price:', openPrice);
            console.log('Current Price:', currentPrice);
            console.log('Return PnL:', returnPnl.toFixed(2));
            console.log('Percentage Increase:', percentageIncrease, '%');
        } else {
            console.log('Not all required numeric fields have values. Cannot calculate return pnl.');
            // Clear the return pnl field if input is incomplete
            $('#id_return_pnl').val('');
        }
    }
});
