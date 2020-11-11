subdirs = document.getElementsByClassName("breadcrumb-nav")[0].children[1].children[0].children
fullName = subdirs[subdirs.length-1].children[0].children[0].getAttribute("title")
fullName = fullName.replace(/[/\\?%*:|"<>]/g, '-')
id = fullName.substring(0,8)

topics = document.getElementsByClassName("ctopics topics row-fluid")[0].children
//iterate through weeks
videos = []
for (topic of topics) {
	content = topic.getElementsByClassName("content")[0]
	weekName = content.children[0].textContent
	weekName = weekName.replace(/[/\\?%*:|"<>]/g, '-')

	videoEntries = content.querySelectorAll(".activity.modtype_kalvidres.kalvidres,.activity.kalvidpres.modtype_kalvidpres")
	//console.log(videoEntries)
	for (entry of videoEntries) {
		//Check if the video has a URL. If it doesn't, it's likely restricted
		if (entry.getElementsByClassName("aalink").length == 0){
			continue
		}
		link = entry.getElementsByClassName("aalink")[0].getAttribute("href")

		entryText = entry.textContent
		videoName = entryText.substring(0,entryText.length-" Kaltura Video Resource".length)
		videoName = videoName.replace(/[/\\?%*:|"<>]/g, '-')

		o = {
			'course':fullName,
			'courseID':id,
			'week':weekName,
			'name':videoName,
			'pageUrl':link
		}
		videos.push(o)
	}
}
return videos