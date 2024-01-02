// Define chart options
const chartOptions = ['hourly', 'daily', 'monthly', 'yearly'];

// Get chart select element
const chartSelect = document.getElementById('time_interval');

// Function to cycle through charts
function cycleChart(direction) {
    const currentIndex = chartOptions.indexOf(chartSelect.value);
    let newIndex = (currentIndex + direction + chartOptions.length) % chartOptions.length;
    chartSelect.value = chartOptions[newIndex];
    submitForm();
}

$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});
function submitForm() {
    document.getElementById("timeIntervalForm").submit();
}

