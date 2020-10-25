
//download function ripped from 
//https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
//https://www.sitepoint.com/delay-sleep-pause-wait/
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
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
	//console.log(weekName)

	videoEntries = content.querySelectorAll(".activity.modtype_kalvidres.kalvidres,.activity.kalvidpres.modtype_kalvidpres")
	//console.log(videoEntries)

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
			'pageUrl':link
		}
		videos.push(o)
	}
}
//videosJSON = JSON.stringify(Object.assign({}, videos));
//download(id+(new Date()).toISOString()+".json", videosJSON)

for (video of videos) {
	var win = window.open(video.pageUrl)
	win.video = video
	win.onload = function(){
		sleep(4000)
		console.log(this.video)
		iframe = this.document.getElementById("contentframe").contentDocument.getElementById("kplayer_ifp").contentDocument
		videoTag = iframe.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0]
		this.video.url = videoTag.src
		if (videoTag.children.length > 0)
			this.video.sub = videoTag.children[0].src
		this.close()
	}
}

console.log(videos)