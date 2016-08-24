# Chromecast-Photo-Frame
A Python script sending randomly picked photos from a computer or NAS to a Chromecast whenever the Chromecast is not used for playing other media. Simply a Photo Frame using Chromecast and your NAS. No need to upload a whole bunch of personal photos to Google Photo in order have a personal photo frame.

The script is more a proof of concept for anyone to be inspired by or develop further. Features that could be useful are:
- Filtering: Display only photos meeting or not meeting a certain criteria.
- Webinterface for setting preferences

I am using the script to cast photos from my Synology NAS to Chromecast, making my TV a photo frame displaying my photos randomly. The script is loaded at boot and will cast photos whenever my Chromecast is idle.

# Dependencies
- A Google Chromecast dongle
- Python 2.7
- pyChromecast library (https://github.com/balloob/pychromecast)
