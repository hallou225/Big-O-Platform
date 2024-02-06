function showUsernameAndPassword() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    var testingDiv = document.getElementById("testingDiv");
    testingDiv.innerHTML = "<p>Username: " + username + "</p><p>Password: " + password + "</p>";
};
