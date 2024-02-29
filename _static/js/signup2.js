function submitAccount(event) {
    /* This function saves the user's first and last name and 
       redirects them to the next page for creating an account */
    
    /* Prevent default behavior from ovewriting what we want the function to do */
    event.preventDefault();

    /* Open the sign in page in the same tab */
    window.open("../", "_self");

}
