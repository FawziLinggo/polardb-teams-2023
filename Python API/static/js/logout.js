import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();
function logout() {
    signOut(auth).then(() => {
        window.location.href = "/login";
    }).catch((error) => {
        console.log(error);
    });
}
document.getElementById("logout").addEventListener("click", logout);