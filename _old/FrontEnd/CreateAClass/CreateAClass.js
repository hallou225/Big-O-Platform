function selectOption(value, type) {
    /* This function DOES NOT YET HAVE A DESCRIPTION */

}

function submitClass(event) {
    /* This function saves the information about the newly created class and 
       redirects the teacher back to the teacher console page */
    
    /* Prevent default behavior from ovewriting what we want the function to do */
    event.preventDefault();

    /* Open the next page in the same tab */
    window.open("../TeacherConsole/TeacherConsole.html", "_self");

}
