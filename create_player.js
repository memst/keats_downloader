//Make sure that a player frame is avilable
//This script should be run from "contentframe"


//Attempt to get the player frame
iframe2 = document.getElementById("kplayer_ifp")

//if kplayer is not loaded, load it manually
if (iframe2 == null) {
	console.log("Manually loading player frame")
	//findClosingCurl adopted from https://stackoverflow.com/a/12752226
	function findClosingCurl(text, openPos) {
	    closePos = openPos;
	    counter = 1;
	    while (counter > 0) {
	        c = text.charAt(++closePos);
	        if (c == '{') {
	            counter++;
	        }
	        else if (c == '}') {
	            counter--;
	        }
	    }
	    return closePos;
	}
	html = document.documentElement.innerHTML

	start = html.indexOf("var settings = {")
	end = findClosingCurl(html,start+15)+1
	settings = html.substring(start,end)
	eval(settings)

	iframe2url = "https://cdnapisec.kaltura.com/html5/html5lib/v2.84.1/mwEmbedFrame.php?&cache_st="+settings.cache_st+"&wid="+settings.wid+"&uiconf_id="+settings.uiconf_id+"&entry_id="+settings.entry_id+"&flashvars[localizationCode]=en&protocol=https"

	iframe2 = document.createElement("iframe")
	
	iframe2.src = iframe2url
	iframe2.id = "kplayer_ifp"
	document.body.appendChild(iframe2)
}
