
function createNewModule() {
    /* This function opens "Create a Class" page */
    window.open("./createModule", "_self");
}




function openDeleteClassModal() {
    document.getElementById("deleteClassModal").style.display = "block";
    document.getElementById("dimBackground").style.display = "block";
}

function closeDeleteClassModal() {
    document.getElementById("deleteClassModal").style.display = "none";
    document.getElementById("dimBackground").style.display = "none";
}


/*
<button>Edit Class Info</button>

<button onclick="openDeleteClassModal()">Delete Class</button>

<!-- Div for dimming the page when the delete class modal is open -->
<div id="dimBackground"></div>

<!-- Div for second chance for user after clicking delete -->
<div id="deleteClassModal">
    <h3>Are you sure you want to delete your class, {{teacher_class.class_name}}?</h3>
    <p>CAUTION: Proceeding will delete your class and all related data.</p>
    <p>The action is IRREVERSIBLE.</p>

    <form method="POST" action="">
        {% csrf_token %}
        <button onclick="closeDeleteClassModal()">Cancel</button>
        <button>Delete Class</button>
    </form>
</div>
*/