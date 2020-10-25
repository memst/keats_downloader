video = document.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0]
videoUrl = video.getAttribute("src")
subtitleUrl = video.getElementsByTagName("track")[0].getAttribute("src")
