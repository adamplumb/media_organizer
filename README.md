# media_organizer
Process a folder of heterogeneous photos and videos and move them to a date-based folder structure.

This is a python script that I wrote to organize 10 years of random photos and videos that I had taken and which were
piling up.  It converts something like this:

	Stuff/
		SwimMeet/ (10 photos, 2 videos)
		2015-03-23/ (1 photo, 1 video)
		DFSEFDFD/ (5 videos)
			Subfolder1/ (1 photo)
			Subfolder2/ (1 photo, 2 videos)

into this:

	Photos/
		2015/
			03/ (11 photos)
			04/ (2 photos)
	Videos/
		2015/
			03/ (3 videos)
			04/ (2 videos)
			05/ (5 videos)

It does this by walking the source folder, infering the date the photo or video was taken by looking at the file name, last modified date, or the EXIF data.  It supports most photo categories including some RAW formats that I have used.

### Usage

	$ python media_organizer.py <SOURCE> <DEST>

### Dependencies

You'll need ufraw-batch installed for RAW files the Python Image Library for gathering EXIF data.

### Notes

 * FYI this will move the files from the source location to the destination, so you may want to make a backup copy of your data before entrusting it with this script.