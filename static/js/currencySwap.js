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


    // Function to format numbers with '+' or '-<i class="fas fa-dollar-sign fa-1x txt-dk-grey p-1 mb-1 mt-1">'
    function formatNumber(text) {
        return text.startsWith('-') ? '-' + '<i class="fas fa-dollar-sign fa-1x p-1 mb-1 mt-1 txt-dk-grey">' + `<span class="font-style-m">` + text.slice(1)  + `</span>` + `</i>`  : '<i class="fas fa-dollar-sign fa-1x p-1 mb-1 mt-1 txt-dk-grey">' + `<span class="font-style-m">` + text + `</span>` + `</i>`;
    }

    // Get all elements with the class swap-symbols
    var elements = document.querySelectorAll('.swap-symbols');

    // Loop through each element
    elements.forEach(function (element) {
        // Get the text content
        var text = element.textContent.trim();

        // Check if the number is positive and update the text and class accordingly
        if (parseFloat(text) < 0) {
            text = formatNumber(text);
            element.classList.add('negative');
        } else {
            text = '+' + formatNumber(text);
            element.classList.add('positive');
        }

        // Update the element with the formatted text
        element.innerHTML = text;
    });
});


