import { getAuth } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();
const user = auth.currentUser;
const userId = user.uid;

console.log(userId);