hides = document.getElementsByClassName("accesshide")
for (hide of hides) {
	if (hide.textContent.localeCompare(" Kaltura Video Resource") == 0) {
		//name, course, week, URL
		nameElement = hide.parentElement
		nameElementText = nameElement.textContent
		name = nameElementText.substring(0, nameElementText.length-" Kaltura Video Resource".length)
		console.log(name)

		console.log(nameElement)
	}
}