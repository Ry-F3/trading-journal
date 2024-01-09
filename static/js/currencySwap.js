document.addEventListener('DOMContentLoaded', function () {
    // Get all elements with the class return-pnl-display
    var elements = document.querySelectorAll('.return-pnl-display');

    // Loop through each element
    elements.forEach(function (element) {
        // Get the text content
        var text = element.textContent.trim();

        // Check if the number is positive and update the text and class accordingly
        if (!text.includes('-')) {
            text = '+' + text;
            element.classList.add('positive');
        } else {
            // Swap '$' and '-'
            text = text.replace('$', '_temp_').replace('-', '$').replace('_temp_', '-');
            element.classList.add('negative');
        }

        // Update the element with the formatted text
        element.textContent = text;
    });
});