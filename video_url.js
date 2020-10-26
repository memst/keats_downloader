iframe1 = window.document.getElementById("contentframe").contentDocument

iframe2 = iframe1.getElementById("kplayer_ifp").contentDocument
if (iframe2 == null) {
	iframe2 = 
}

videoTag = iframe.getElementsByClassName("persistentNativePlayer nativeEmbedPlayerPid")[0]

url = videoTag.src
sub = null;
if (videoTag.children.length > 0)
	sub = videoTag.children[0].src

return [url,sub]