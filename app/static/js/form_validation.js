function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    if (password != confirmPassword) {
        var modal = document.getElementById("customModal");
        var span = document.getElementsByClassName("close")[0];

        modal.style.display = "block"; // Show the modal

        span.onclick = function() {
            modal.style.display = "none"; // Hide the modal when the close button is clicked
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none"; // Hide the modal when clicking outside of it
            }
        };

        return false; // Prevent form submission
    }
    return true; // Allow form submission
}
