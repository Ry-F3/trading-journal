// Form Calculations
// Global Variables
console.log("global");
var isShortSelected = false;
var isLongSelected = false;

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

        // Calculate Return PnL
        var returnPnl = (percentageLongChange / 100) * margin;

        // Update the return_pnl field
        $('#id_return_pnl').val(returnPnl.toFixed(2));

    } else {
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

        // Calculate Return PnL
        var returnPnl = (percentageShortChange / 100) * margin;

        // Update the return_pnl field
        $('#id_return_pnl').val(returnPnl.toFixed(2));

    } else {
        // Clear the return pnl field if input is incomplete
        $('#id_return_pnl').val('');
    }
}

// Call the function to check and enable/disable fields when needed
checkSelectionAndEnableFields();

$(document).ready(function () {
    // jQuery code
    $('#id_leverage, #id_margin, #id_open_price, #id_current_price').on('input', function () {

        if (isLongSelected) {
            performLongCalculations();
            // Call the function to enable or disable fields based on edit mode
        } else if (isShortSelected) {
            performShortCalculations();
            // Call the function to enable or disable fields based on edit mode
        } else {
            // Call the function to enable or disable fields based on edit mode
        }
    });

    
});

function longShortHandler() {
    if (isLongSelected) {
        longCalculation();
        checkSelectionAndEnableFields();
    } else if (isShortSelected) {
        shortCalculation();
        checkSelectionAndEnableFields();
    }


    function longCalculation() {
        // Your long calculation logic here
        clearInputValues();
        performLongCalculations(); // Call the common calculation logic
    }

    function shortCalculation() {
        // Your short calculation logic here
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

// Smooth scroll on anchor click
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});