import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();

var email = '';
var password = '';

// listener input email
document.getElementById("email").addEventListener("input", function (event) {
    email = event.target.value;
});
// listener input password
document.getElementById("password").addEventListener("input", function (event) {
    password = event.target.value;
});

function signup() {
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        const user = userCredential.user;
        var root_url = window.location.origin;
        console.log("root url : "+root_url)
        fetch(root_url + '/register', {
            method: 'POST',
            body: JSON.stringify({
                id: user.uid,
                email: email,
                password: password,
                username: email.split('@')[0],
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            }
        })
        .then(function (response) {
            if (response.ok) {
                window.location.href = "/";
            }
            console.log('response', response);
            alert('Gagal');
            return Promise.reject(response);
        })
        .catch(function (error) {
            console.log(error);
            alert(error);
        });
    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log(errorCode, errorMessage);
        alert(errorMessage);
    });
}

// listener click button sign in with id login
document.getElementById("submit").addEventListener("click", signup);
