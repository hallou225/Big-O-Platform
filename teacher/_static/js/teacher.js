var username = "Henri";

window.onload = () => {
    if (username[username.length - 1] == 's') {
        document.getElementById("mainHeading").innerHTML = username + "' Classes";
    } else {
        document.getElementById("mainHeading").innerHTML = username + "'s Classes";
    }
}

function openClass() {
    /* This function allows the instructor to access the main page for their selected class */
    
    window.open("https://www.google.com", "_blank");

}

function createNewClass() {
    /* This function opens "Create a Class" page */

    window.open("./createclass", "_self");

}
