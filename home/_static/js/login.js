function togglePasswordVisibility() {
    /* This function allows the user to show/hide their password on the screen (password hidden by default) */
    
    var passwordInput = document.getElementById("password");    // Locate the password text entry

    if (passwordInput.type === "password") {
        passwordInput.type = "text";        // Show the user's password
    } else {
        passwordInput.type = "password";    // Hide the user's password
    }
}