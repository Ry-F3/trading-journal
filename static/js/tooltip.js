  // JavaScript to close alerts after a delay
  window.setTimeout(function () {
    $(".alert").fadeTo(300, 0).slideUp(300, function () {
        $(this).remove();
    });
}, 3500);