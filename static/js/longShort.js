// Long/Short Dropdown Handling using Event Delegation
$(document).on('change', '#id_long_short', function () {
    var selectedValue = $(this).val();

    // Handle the selected value (long or short)
    if (selectedValue === 'long') {
        isLongSelected = true;
        isShortSelected = false;
        longShortHandler();
        // Add additional logic for Long position if needed
    } else if (selectedValue === 'short') {
        isShortSelected = true;
        isLongSelected = false;
        longShortHandler();
        // Add additional logic for Short position if needed
    }

}); 