function sendMail(contactForm) {
    emailjs.send("service_p7moexb", "template_nom1zmn", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "suggestion_request": contactForm.message.value
    })
        .then(
            function (response) {
                console.log("SUCCESS", response);
                // Check if the email was successfully sent
                if (response.status === 200) {
                    // Show the thank you message
                    showThankYouMessage();
                } else {
                    // Handle other success responses or consider them as failures
                    console.log("Email not sent successfully. Handle accordingly.");
                }
            },
            function (error) {
                console.log("FAILED", error);
                // Handle the error response
            });
    return false;
}

function showThankYouMessage() {
    // Hide the contact form container
    document.getElementById('containerForm').style.display = 'none';

    // Show the thank you message
    var thankYouContainer = document.getElementById('thankYouContainer');
    thankYouContainer.style.display = 'block';
}