function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

subdirs = document.getElementsByClassName("breadcrumb-nav")[0].children[1].children[0].children
fullName = subdirs[subdirs.length-1].children[0].children[0].getAttribute("title")
id = fullName.substring(0,8)

topics = document.getElementsByClassName("ctopics topics row-fluid")[0].children
//iterate through weeks
videos = []
for (topic of topics) {
	content = topic.getElementsByClassName("content")[0]
	weekName = content.children[0].textContent
	console.log(weekName)

	videoEntries = content.querySelectorAll(".activity.modtype_kalvidres.kalvidres,.activity.kalvidpres.modtype_kalvidpres")
	console.log(videoEntries)

	for (entry of videoEntries) {
		entryText = entry.textContent
		videoName = entryText.substring(0,entryText.length-" Kaltura Video Resource".length)
		videoName = videoName.replace(/[/\\?%*:|"<>]/g, '-')


		link = entry.getElementsByClassName("aalink")[0].getAttribute("href")

		o = {
			'course':fullName,
			'courseID':id,
			'week':weekName,
			'name':videoName,
			'url':link
		}
		videos.push(o)
	}
}
videosJSON = JSON.stringify(Object.assign({}, arr));
download(id, videosJSON)