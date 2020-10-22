import requests as re

courseUrls = [
	"***REMOVED***",
	"***REMOVED***",
	"***REMOVED***",
	"***REMOVED***",
	"***REMOVED***"
]

for courseUrl in courseUrls:
	r = re.get(courseUrl)
