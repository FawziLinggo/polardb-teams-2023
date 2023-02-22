import {getAuth, onAuthStateChanged} from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";

const auth = getAuth();

// get last url from this page
var currentLocation = window.location;
var symbol = currentLocation.toString().split("/").pop();
var local = currentLocation.toString().split("/").slice(0, 3).join("/");

onAuthStateChanged(auth, (user) => {
    console.log(user.uid);
  if (user) {
      var user =user.email.split('@')[0];

     fetch(local+'/leaderboard-data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'data': user,
        }
     }
     ).then(response => response.json())
        .then(data => {
          console.log(data);
          const container = document.getElementById('leaderboard-container');
          const leaderboard = document.createElement('div');
          leaderboard.innerHTML = `Hello: ${data.name}, Your Account Balance is : ${data.balance}`;
          container.appendChild(leaderboard);
        });
  }
});
