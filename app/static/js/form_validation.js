function validatePassword() {
    // Get form values
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;

    // Regular expressions for validations
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

    // Validate first name and last name are not empty
    if (firstName.trim() === "" || lastName.trim() === "") {
        showModal("First name and last name cannot be empty.");
        return false; // Prevent form submission
    }

    // Validate email format
    if (!emailPattern.test(email)) {
        showModal("Please enter a valid email address.");
        return false; // Prevent form submission
    }

    // Validate password complexity
    if (!passwordPattern.test(password)) {
        showModal("Password must be at least 8 characters long, contain at least one number, one uppercase letter, and one lowercase letter.");
        return false; // Prevent form submission
    }

    // Validate password match
    if (password !== confirmPassword) {
        showModal("Passwords do not match.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}function showModal(message) {
    var modal = document.getElementById("customModal");
    var modalMessage = document.getElementById("modalMessage");
    var span = document.getElementsByClassName("close")[0];

    modalMessage.textContent = message;
    modal.style.display = "block"; // Show the modal

    span.onclick = function() {
        modal.style.display = "none"; // Hide the modal when the close button is clicked
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none"; // Hide the modal when clicking outside of it
        }
    };
}

// Add event listener to the form to use custom validation
document.querySelector("form").addEventListener("submit", validatePassword);