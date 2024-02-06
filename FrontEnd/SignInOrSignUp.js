function showUsernameAndPassword() {
    /* This function simply displays the username and password entered onto the screen */
    /* This function is intended for testing purposes only, and will not be included in the actual site */

    var username = document.getElementById("username").value;   // Read input from text input with id="username"
    var password = document.getElementById("password").value;   // Read input from text input with id="password"

    var testingDiv = document.getElementById("testingDiv");     // Locate the testing div in HTML file

    // Add two paragraph elements containing the username and password entered by the user
    testingDiv.innerHTML = "<p>Username: " + username + "</p><p>Password: " + password + "</p>";
};
