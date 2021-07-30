var currentScript = document.currentScript;

document.getElementById("btn-follow").onclick = (event) => {
    
    var pageuser = currentScript.getAttribute('pageuser');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let data = { username: pageuser};
    console.log(data);

    const POSTMethod = {
        method: 'POST',
        mode: 'same-origin',
        redirect: 'follow',
        headers: {'X-CSRFToken': csrftoken, 'Content-type': 'application/json; charset=UTF-8'},
        body: JSON.stringify(data), 
    }

    fetch("follow_unfollow", POSTMethod)
    .then(response => {

        if (response.ok) {
            location.reload();
        }
    });
}