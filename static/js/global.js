// Form Calculations
// Global Variables
var isShortSelected = false;
var isLongSelected = false;
var editMode = false; // Set to true or false based on your logic
var fieldsEnabled = false;
console.log('edit mode', editMode);

console.log("Initial Global values - isLongSelected:", isLongSelected, "isShortSelected:", isShortSelected);

disableFields();


// Function to disable input fields
function disableFields() {
    $('#id_position, #id_leverage, #id_margin, #id_open_price, #id_current_price, #id_return_pnl').prop('disabled', true);
}

// Function to enable input fields
function enableFields() {
    $('#id_position, #id_leverage, #id_margin, #id_open_price, #id_current_price, #id_return_pnl').prop('disabled', false);
}

// Function to clear input values
function clearInputValues() {
    $('#id_leverage, #id_margin, #id_open_price, #id_current_price, #id_return_pnl').val('');
}



// Function to perform calculations
function performLongCalculations() {

    var leverage = parseFloat($('#id_leverage').val()) || 0;
    var margin = parseFloat($('#id_margin').val()) || 0;
    var openPrice = parseFloat($('#id_open_price').val()) || 0;
    var currentPrice = parseFloat($('#id_current_price').val()) || 0;

    // Check if all required numeric fields have values
    var allFieldsFilled = margin && openPrice && currentPrice;

    if (allFieldsFilled) {
        // Calculate percentage Change
        var percentageLongChange = ((currentPrice - openPrice) / openPrice) * leverage * 100;

        // Format percentageChange with two decimal places
        percentageLongChange = percentageLongChange.toFixed(2);

        // Log percentage Change
        console.log('Percentage Change:', percentageLongChange, '%');

        // Calculate Return PnL
        var returnPnl = (percentageLongChange / 100) * margin;

        // Update the return_pnl field
        $('#id_return_pnl').val(returnPnl.toFixed(2));

        console.log('Calculating return pnl');
        // Log relevant variables
        console.log('Margin:', margin);
        console.log('Open Price:', openPrice);
        console.log('Current Price:', currentPrice);
        console.log('Return PnL:', returnPnl.toFixed(2));
        console.log('Percentage Change:', percentageLongChange, '%');
    } else {
        console.log('Not all required numeric fields have values. Cannot calculate return pnl.');
        // Clear the return pnl field if input is incomplete
        $('#id_return_pnl').val('');
    }
}

function performShortCalculations() {

    var leverage = parseFloat($('#id_leverage').val()) || 0;
    var margin = parseFloat($('#id_margin').val()) || 0;
    var openPrice = parseFloat($('#id_open_price').val()) || 0;
    var currentPrice = parseFloat($('#id_current_price').val()) || 0;

    // Check if all required numeric fields have values
    var allFieldsFilled = margin && openPrice && currentPrice;

    if (allFieldsFilled) {
        // Calculate percentage Change
        var percentageShortChange = ((openPrice - currentPrice) / openPrice) * leverage * 100;

        // Format percentageChange with two decimal places
        percentageShortChange = percentageShortChange.toFixed(2);

        // Log percentage Change
        console.log('Percentage Change:', percentageShortChange, '%');

        // Calculate Return PnL
        var returnPnl = (percentageShortChange / 100) * margin;

        // Update the return_pnl field
        $('#id_return_pnl').val(returnPnl.toFixed(2));

        console.log('Calculating return pnl');
        // Log relevant variables
        console.log('Margin:', margin);
        console.log('Open Price:', openPrice);
        console.log('Current Price:', currentPrice);
        console.log('Return PnL:', returnPnl.toFixed(2));
        console.log('Percentage Change:', percentageShortChange, '%');
    } else {
        console.log('Not all required numeric fields have values. Cannot calculate return pnl.');
        // Clear the return pnl field if input is incomplete
        $('#id_return_pnl').val('');
    }
}

// Call the function to check and enable/disable fields when needed
checkSelectionAndEnableFields();

$(document).ready(function () {
    // jQuery code
    $('#id_leverage, #id_margin, #id_open_price, #id_current_price').on('input', function () {
        console.log('Input event triggered');

        if (isLongSelected) {
            console.log('Long calculation selected.');
            performLongCalculations();
            // Call the function to enable or disable fields based on edit mode
        } else if (isShortSelected) {
            console.log('Short calculation selected.');
            performShortCalculations();
            // Call the function to enable or disable fields based on edit mode
        } else {
            console.log('No calculation type selected.');
            // Call the function to enable or disable fields based on edit mode
        }
    });

    
});

function longShortHandler() {
    if (isLongSelected) {
        console.log('User has made a Long calc selection.');
        longCalculation();
        checkSelectionAndEnableFields();
    } else if (isShortSelected) {
        console.log('User has made a Short calc selection.');
        shortCalculation();
        checkSelectionAndEnableFields();
    }

    console.log("Post Global Initiating Function - isLongSelected:", isLongSelected, "isShortSelected:", isShortSelected);

    function longCalculation() {
        // Your long calculation logic here
        console.log("Executing Long Calculation");
        clearInputValues();
        performLongCalculations(); // Call the common calculation logic
    }

    function shortCalculation() {
        // Your short calculation logic here
        console.log("Executing Short Calculation");
        checkSelectionAndEnableFields();
        clearInputValues();
        performShortCalculations(); // Call the common calculation logic
    }
}

// Function to check selection and enable/disable fields accordingly
function checkSelectionAndEnableFields() {
    if (isLongSelected && isShortSelected) {
        // Both are false, disable fields
        enableFields();
        
    } else if (!isLongSelected && !isShortSelected) {
        disableFields();
    } else {
        enableFields();
    }


}

