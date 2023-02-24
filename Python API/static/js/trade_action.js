import { getAuth } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";
const auth = getAuth()

var amountSpend = 0
var tradeStatus = "Buy"
var statusHeading = document.getElementById("tradeStatusHeading")
statusHeading.innerHTML = "Buy"

// Memakai substring supaya hanya nama perusahaan yang di output 
var currentLocation = window.location;
var symbol = currentLocation.toString().split("/").pop().substring(0, 4);


// Function Convert nomor ke Rupiah

//  Status Pilihan Buy atau Sell
function tradeSwitchStatus(status) {
  statusHeading.innerHTML = status
  tradeStatus = status
}


// Button Buy dan Sell
document.getElementById("btnBuy").addEventListener("click", function () {
  tradeSwitchStatus("Buy")
})
document.getElementById("btnSell").addEventListener("click", function () {
  tradeSwitchStatus("Sell")
})

// Input Amount
document.getElementById("amount").addEventListener("input", function (event) {
  amountSpend = event.target.value
})


// Action Send Email Order 
function sendEmailOrder(id, coop, amount, status) {
  const tradeData = {
    id: id,
    stock: coop,
    amount: amount,
    status_trade: status.toLowerCase()
  }
  console.log(status)
  fetch("http://47.254.76.121:21891/send-email-order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode:"cors",
    body: JSON.stringify(tradeData)
    
  }).then((response) => {
    if (response.ok) {
      return response
    } else {
      throw new Error("Email gagal Dikirim")
    }
  }).then((data) => {
    var message = `Terima kasih sudah ${status} di ${coop}! Cek email anda`
    console.log({
      data,
      message
    })
    alert(message)
  }).catch((error) => {
    console.log(error)
  })
}

function sendEmailSubs(id, coop) {
  const tradeData = {
    id: id,
    stock: coop,
  }

  fetch("http://47.254.76.121:21891/send-email-subscriber", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode:"cors",
    body: JSON.stringify(tradeData)
    
  }).then((response) => {
    if (response.ok) {
      return response
    } else {
      throw new Error("Email gagal Dikirim")
    }
  }).then((data) => {
    var message = `Terima kasih sudah Subscribe di ${coop}!, Silahkan Cek email anda`
    console.log({
      data,
      message
    })
    alert(message)
  }).catch((error) => {
    console.log(error)
  })
}


// Action Subscription 
function subscriptionAction(id, coop) {
    const subsData = {
      id: id,
      stock: coop
    }
    console.log(subsData)
    sendEmailSubs(id,coop)
}
// Action Buy or Sell
function statusTradeAction(id, coop, amount, status) {
  const tradeData = {
    id: id,
    stock: coop,
    amount: parseFloat(amount),
    status_trade: status
  }
  console.log(tradeData)
  fetch("http://47.254.76.121:21891/investors-net-balance", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    mode:"cors",
    body: JSON.stringify(tradeData)
  }).then((response) => {
    if (response.ok) {
      return response
    } else {
      throw new Error("Data Failed to be Added")
    }
  }).then((data) => {
    console.log({
      data,
      message: "Data berhasil dikirim"
    })

  }).catch((error) => {
    console.log(error)
  })
}

// Action Trade Now
function tradeAction(status, amount, coop, id) {
    statusTradeAction(id, coop, amount, status)
    sendEmailOrder(id, coop, amount, status)
}

// Tombol Subs
document.getElementById("btnSubs").addEventListener("click",function () {
  subscriptionAction(auth.currentUser.uid, symbol)

})

// Tombol Trade Now
document.getElementById("submit").addEventListener("click", function () {
  if (confirm("Konfirmasi Transaksi?") == true) {
    tradeAction(tradeStatus, amountSpend, symbol, auth.currentUser.uid)
  }
})

