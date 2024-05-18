function validatePassword() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;
    if (password != confirmPassword) {
        alert("Passwords do not matches.");
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}
