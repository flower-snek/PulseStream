
chrome.runtime.onConnect.addListener(port => {
  console.log('connected ', port);

  if (port.name === 'hi') {
    port.onMessage.addListener(this.processMessage);
  }
});
chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
	active_pulsus = url.startsWith("https://www.pulsus.cc") || url.startsWith("https://pulsus.cc");
	if(!active_pulsus){
		document.getElementById("pulsus_popup").innerHTML = "you've gotta be on pulsus gamma.";
	}else{
		let percent = 0;
		document.getElementById("pulsus_popup").innerHTML = "if you have the python script open you should now see it either showing a bunch of question marks or your last score. if not uhhhhhhhhh lmk?";
	}
});

console.log("Hello world!");