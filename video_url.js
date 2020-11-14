videoTag = document.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0]

url = videoTag.src
sub = null;
if (videoTag.children.length > 0)
	sub = videoTag.children[0].src

return [url,sub]