function getUrls() {
	let videoTag;
	let fulfill;
	const promise = new Promise(x => fulfill = x);
	checkTag();
	return promise;

	function checkTag() {
		videoTag = document.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0];
		if (videoTag != undefined) {
			checkVideo();
		} else {
			setTimeout(checkTag, 100);
		}
	}
	function checkVideo() {
		try {
			console.log("Checking for video...");
			if (videoTag.src != undefined && videoTag.src != "") {
				checkSubtitles(0);
			} else
				setTimeout(checkVideo, 100);
			}
		catch {
			setTimeout(checkVideo, 100);
		}
	}
	function checkSubtitles(counter) {
		//The counter prevents the script from waiting forever in case the subtitles don't actually exist.
		if (counter < 5) {
			console.log("Checking for subtitles...");
			if (videoTag.children.length > 0) {
				var url = videoTag.src;
				var sub = videoTag.children[0].src;
				fulfill([url, sub]);
			}
    		else {
    			setTimeout(checkSubtitles.bind(this, counter+1), 100);
    		}
		} else {
			var url = videoTag.src;
			fulfill([url, null])
		}
		
	}
}
return await getUrls();