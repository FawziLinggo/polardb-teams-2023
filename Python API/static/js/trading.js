import { getAuth } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();
const user = auth.currentUser;
const userId = user.uid;
// TODO: Change the path to your own path
function buy() {
    var root_url = window.location.origin;
    fetch(root_url + '/your_api', {
        method: 'POST',
        body: JSON.stringify({
            // TODO: Change the data to your own data
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    })
    .then(function (response) {
        if (response.ok) {
            // TODO: If the response is ok, do something
        }
    })
    .catch(function (error) {
        console.log(error);
        alert(error);
    });
}
// TODO: Change the path to your own path
function sell() {
    var root_url = window.location.origin;
    fetch(root_url + '/your_api', {
        method: 'POST',
        body: JSON.stringify({
            // TODO: Change the data to your own data
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        }
    })
    .then(function (response) {
        if (response.ok) {
            // TODO: If the response is ok, do something
        }
    })
    .catch(function (error) {
        console.log(error);
        alert(error);
    });
}

document.getElementById("buy").addEventListener("click", buy);
document.getElementById("sell").addEventListener("click", sell);
