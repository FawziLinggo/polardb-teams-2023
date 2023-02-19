const url_websockets = "ws://172.18.46.121:8765";
const ws = new WebSocket(url_websockets);
console.log(ws);

// get last url from this page
var currentLocation = window.location;
var symbol = currentLocation.toString().split("/").pop();
var local = currentLocation.toString().split("/").slice(0, 3).join("/");

// VERBOSE
// console.log(symbol);
// console.log(local);

// sent symbol to server using http post method
const url_post = local + "/symbol";
const data = { symbol: symbol };

// get data from fetch
const response = fetch(url_post,  {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    mode: 'no-cors'
});

var chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 500,
  height: 430,
    layout: {
backgroundColor: '#000000',
    },
	grid: {
		vertLines: {
			color: '#363c4e',
		},
		horzLines: {
			color: '#363c4e',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	PriceScale: {
		borderColor: '#cccccc',
	},
	timeScale: {
		borderColor: '#cccccc)',
        timeVisible: true,
	},
});

var candleSeries = chart.addCandlestickSeries();
let currentBar = {};
let trades = [];

const trade = document.getElementById("trade");
ws.onmessage = function (event) {
    messages = JSON.parse(event.data);
    // console.log(messages);
        if (messages.symbol == symbol) {
            const tradeElement = document.createElement("div");
            tradeElement.className = "trade";
            tradeElement.innerHTML = `<b>${messages.symbol}</b> 
        ${messages.close} ${messages.high} ${messages.low} 
        ${messages.open} ${messages.time}`;
            trade.appendChild(tradeElement);

            // var bar = messages[Key];
            var timestamp = new Date(messages.time).getTime() / 1000;


            currentBar = {
                time: timestamp,
                open: messages.open,
                high: messages.high,
                low: messages.low,
                close: messages.close,
            };

            var element = document.getElementsByClassName("trade");
            if (element.length > 19) {
                trade.removeChild(element[0]);
            }

            candleSeries.update(currentBar);
        }
}