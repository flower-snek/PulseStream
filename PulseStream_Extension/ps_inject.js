let disconnect_count = 0

console.log("PulseStream: Injection successful");

function connect(){
	let ws = new WebSocket('ws://localhost:3757');
	//console.log(ws)
	let interval_id = -1;

	ws.onopen = function(event) {
		console.log("PulseStream: Websocket connection opened");
		disconnect_count = 0;
		ws.send("Hello /e");
		clearInterval(interval_id);
		interval_id = setInterval(()=>{
			let sending_object = {
				acc: ut.acc,
				hitStats: ut.hitStats,
				title: ut.title,
				stars: ut.stars,
				sel_id: mt[ft.lvl.sel],
				mods: ut.mods,
				score: ut.score,
				playing: ut.songPlaying
			}
			ws.send(JSON.stringify(sending_object));
		}, 200);
	};

	ws.onclose = function(event) {
		disconnect_count++;
		console.log("PulseStream: Websocket connection closed");
		clearInterval(interval_id);
		console.log("PulseStream: Attempting reconnect in " + (2**disconnect_count) + " seconds...");
		setTimeout(()=>{
			connect();
		}, (2**disconnect_count)*2000);
	};
}
connect();