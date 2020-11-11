function processPlayerContents(iframe) {
	console.log(iframe)
	videoTag = iframe.contentDocument.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0]

	window.url = videoTag.src
	if (videoTag.children.length > 0)
		window.sub = videoTag.children[0].src

	document.title = 'Urls received'
	//return [url,sub]
}


iframe1 = window.document.getElementById("contentframe").contentDocument
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
	html = iframe1.documentElement.innerHTML

	start = html.indexOf("var settings = {")
	end = findClosingCurl(html,start+15)+1
	settings = html.substring(start,end)
	eval(settings)

	iframe2url = "https://cdnapisec.kaltura.com/html5/html5lib/v2.84.1/mwEmbedFrame.php?&cache_st="+settings.cache_st+"&wid="+settings.wid+"&uiconf_id="+settings.uiconf_id+"&entry_id="+settings.entry_id+"&flashvars[localizationCode]=en&protocol=https"

	iframe2 = iframe1.createElement("iframe")
	
	iframe2.src = iframe2url
	iframe2.id = "kplayer_ifp"
	iframe1.body.appendChild(iframe2)
}

//process player contents
iframe2.addEventListener("load", processPlayerContents(iframe2))

