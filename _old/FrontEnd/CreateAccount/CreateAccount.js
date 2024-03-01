function nextPage(event) {
    /* This function saves the user's first and last name and 
       redirects them to the next page for creating an account */
    
    /* Prevent default behavior from ovewriting what we want the function to do */
    event.preventDefault();

    /* Open the next page in the same tab */
    window.open("../CreateAccount/CreateAccount2.html", "_self");

}
