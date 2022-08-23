//get full module name and id
subdirs = document.getElementsByClassName("breadcrumb-nav")[0].children[1].children[0].children;
fullName = subdirs[subdirs.length-1].children[0].children[0].getAttribute("title");
fullName = fullName.replace(/[/\\?%*:|"<>]/g, '-');
id = fullName.substring(0,8);

topics = document.getElementsByClassName("ctopics topics row")[0].children;
//iterate through weeks
videos = [];
for (topic of topics) {
    content = topic.getElementsByClassName("content")[0];
    weekName = content.children[0].getElementsByClassName("sectionname")[0].innerHTML
    weekName = weekName.replace(/[/\\?%*:|"<>]/g, '-');

    videoEntries = content.querySelectorAll(".activity.modtype_kalvidres.kalvidres,.activity.kalvidpres.modtype_kalvidpres");
    //console.log(videoEntries)
    for (entry of videoEntries) {
        //Check if the video has a URL. If it doesn't, it's likely restricted
        if (entry.getElementsByClassName("aalink").length == 0){
            continue;
        }
        link = entry.getElementsByClassName("aalink")[0].getAttribute("href");

        // Remove kaltura text
		entry.getElementsByClassName("instancename")[0].children[0].remove()

		videoName = entry.getElementsByClassName("instancename")[0].innerHTML
		videoName = videoName.replace(/[/\\?%*:|"<>]/g, '-')

        o = {
            'course_name':fullName,
            'course_id':id,
            'week':weekName,
            'video_name':videoName,
            'page_url':link
        };
        videos.push(o);
    }
}
return videos;