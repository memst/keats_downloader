videoEntries = content.getElementsByClassName("activity kalvidres modtype_kalvidres ")
	console.log(videoEntries)

	for (entry of videoEntries) {
		link = entry.getElementsByClassName("aalink")[0].getAttribute("href")
	}