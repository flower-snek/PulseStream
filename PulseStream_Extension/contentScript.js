/*let ws = new WebSocket('ws://localhost:3757'); 

function clickHandler(event) {
		ws.send("Click~");
}
ws.addEventListener("open", (event) => {
	ws.send("Hello!");
	window.addEventListener("click", clickHandler);
});

ws.addEventListener("close", (event) => {
	ws.send("bye o/");
	window.removeEventListener("click", clickHandler);
});
*/

// attempt to inject a data sender

var s = document.createElement('script');
s.src = chrome.runtime.getURL(`ps_inject.js`);
s.onload = function() {
    this.remove();
};
(document.head || document.documentElement).appendChild(s);