import { getAuth, signInWithEmailAndPassword, } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();

var email = '';
var password = '';

// listener input email
document.getElementById("email").addEventListener("input", function (event) {
    email = event.target.value;
    console.log('email', email);
});
// listener input password
document.getElementById("password").addEventListener("input", function (event) {
    password = event.target.value;
});

function login() {
    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
        const user = userCredential.user;
        window.location.href = "/";
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.log(errorCode, errorMessage);
            alert(errorMessage);
        });
}

document.getElementById("submit").addEventListener("click", login);