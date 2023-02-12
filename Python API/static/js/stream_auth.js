import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";
 
const auth = getAuth();
onAuthStateChanged(auth, (user) => {
  if (user) {
    const uid = user.uid;
    if (window.location.pathname == "/login") {
        window.location.href = "/";
    } else if (window.location.pathname == "/signup") {
        window.location.href = "/";
    }
  } else {
    if (window.location.pathname == "/signup") {
      // do nothing
    } else if (window.location.pathname != "/login") {
      window.location.href = "/login";
    }
  }
});