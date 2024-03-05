function submitClass(event) {
    /* This function saves the user's new class information and 
       redirects them to the home page */
    
    /* Prevent default behavior from ovewriting what we want the function to do */
    event.preventDefault();

    /* Open the next page in the same tab */
    window.open("../", "_self");

}
