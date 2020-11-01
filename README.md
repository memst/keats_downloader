> :warning: This project is very WIP, I provide no warranty. Depending on how your lecturer uses KEATS, the link to the video page or the video itself might not be recognised.

# Keats Downloader
This is a project intended to automatically download all videos in a course and store them locally. Benefits include:
- Being able to playback videos at non-turtle speed (more than 2x)
- Being able to use subtitles as a semi-accurate transcript
- Being able to watch high-resolution video streams with no buffering

## Basic usage
1. Create a `courses.txt` file with the urls to all courses you want to download separated by newlines. Its contents should look something like this:
```
https://keats.kcl.ac.uk/course/view.php?id=AAAAA
https://keats.kcl.ac.uk/course/view.php?id=BBBBB
https://keats.kcl.ac.uk/course/view.php?id=CCCCC
https://keats.kcl.ac.uk/course/view.php?id=DDDDD
```
2. Execute the python files in their numbered order. The 0-numbered files should be executed only once, others will have to be reapeated if you want to download new videos. `0_login.py` gives you an opportunity to login to your keats account because the browser uses a separate profile.

You still need to have logged in to your account to use this.