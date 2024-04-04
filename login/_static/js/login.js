/*
function togglePasswordVisibility() {
    // This function allows the user to show/hide their password on the screen (password hidden by default) /
    
    var passwordInput = document.getElementById("password");    // Locate the password text entry

    if (passwordInput.type === "password") {
        passwordInput.type = "text";        // Show the user's password
    } else {
        passwordInput.type = "password";    // Hide the user's password
    }
}
*/

function togglePasswordVisibility() {
    // This function allows the user to show/hide their password on the screen (password hidden by default) /
    
    var passwordInput = document.getElementById("form_password");    // Locate the password text entry

    if (passwordInput.type === "password") {
        passwordInput.type = "text";        // Show the user's password
    } else {
        passwordInput.type = "password";    // Hide the user's password
    }
}

/*
function checkCredentials(event) {
    // This function alerts a message based on whether the credentials are valid

    // Prevent default behavior from overwriting what we want the function to do
    event.preventDefault();

    var username = document.getElementById("username").value;   // Read input from text input with id="username"
    var password = document.getElementById("password").value;   // Read input from text input with id="password"
*/

    /* Loop through the students table */
    
        /* If username exists in the students table */

            /* If password matches */
                /* Redirect the user the student page */
                /* return */

            /* If password does NOT match */
                /* Tell the user the password they entered is incorrect */
                /* Clear only the password text entry */
                /* return */

        /* If the username does NOT exist in the students table */
            /* Loop through the teachers table */

                /* If password matches */
                    /* Redirect the user the teacher page */
                    /* return */

                /* If password does NOT match */
                    /* Tell the user the password they entered is incorrect */
                    /* Clear only the password text entry */
                    /* return */
        
        /* If the username does NOT exist in either table */
            /* Tell the user the username they entered is not associated with a registered account */

/*

    let usersTableLength = usersTable.length;   // Number of users in usersTable

    for (let i = 0; i <= (usersTableLength - 1); i++) {     // Iterating through the usersTable

        if ( (username == usersTable[i].username) && (password == usersTable[i].password) ) {
            alert("Congratulations!!! The provided credentials are valid!");    // Output for valid credentials
            if (usersTable[i].role == "teacher") {
                //Open the next page in the same tab
                window.open("teacher", "_self");
            }
            break;
        }

        else if (i == usersTableLength - 1) {
            alert("The provided credentials are INVALID!!!");    // Output for invalid credentials
        }

    }
    
*/
    
// }

/*
let user1 = {
    uniqueID: "user1",
    email: "user1@gmail.com",
    username: "testingUsername1",
    password: "testingPassword1",
    role: "teacher"
};

let user2 = {
    uniqueID: "user2",
    email: "user2@gmail.com",
    username: "testingUsername2",
    password: "testingPassword2",
    role: "student"
};

let user3 = {
    uniqueID: "user3",
    email: "user3@gmail.com",
    username: "testingUsername3",
    password: "testingPassword3",
    role: "student"
};

let usersTable = [
    user1, 
    user2, 
    user3
];
*/
