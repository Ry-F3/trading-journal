   // Long/Short Dropdown Handling using Event Delegation
   $(document).on('change', '#id_long_short', function () {
    console.log("hello");
    var selectedValue = $(this).val();
    console.log('Dropdown changed. Selected value:', selectedValue);

    // Handle the selected value (long or short)
    if (selectedValue === 'long') {
        console.log('User selected Long position.');
        isLongSelected = true;
        isShortSelected = false;
        console.log('L:', isLongSelected);
        console.log('S:', isShortSelected);
        // Add additional logic for Long position if needed
    } else if (selectedValue === 'short') {
        console.log('User selected Short position.');
        isShortSelected = true;
        isLongSelected = false;
        console.log('L:', isLongSelected);
        console.log('S:', isShortSelected);
        // Add additional logic for Short position if needed
    }
});