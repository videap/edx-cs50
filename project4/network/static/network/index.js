document.addEventListener('DOMContentLoaded', function() {

    // create form actions
    document.getElementById("new_post").onclick = (event) => show_form();

    // cancel form actions
    document.querySelectorAll("#close_form").forEach( item => {
        item.onclick = (event) => cancel_form();
    });

});

function show_form(post_content) {
    document.querySelectorAll(".body_content").forEach( (item) => {
        item.style.opacity= 0.15;
    });

    if (post_content !== undefined) {
        document.getElementById("post_form_content").innerHTML = post_content;
    }


    document.querySelector("#new_post_form").style.display="block";

}

function cancel_form () {
    event.preventDefault();
        document.querySelectorAll(".body_content").forEach( (item) => {
            item.style.opacity= 1;
        });
        
        document.querySelector("#new_post_form").style.display="none";
        document.querySelector("#edit_post_form").style.display="none";
}