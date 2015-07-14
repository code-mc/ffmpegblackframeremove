# FFMPEG Black removal script

Inspired by the superuser post [here](http://superuser.com/questions/692489/automatically-split-large-mov-video-files-into-smaller-files-at-black-frames-s). This script removes all black sections in a by FFMPEG supported video. There's a couple params you can tweak, the default ones are tested and confirmed working.


### Usage

1. First up you'll have to download FFMPEG yourself, which can be found [here](http://ffmpeg.zeranoe.com/builds/). 
2. Put the ffmpeg.exe file in the appropriate location (indicated by the file called "ffmpegEXEgoeshere").
3. Stash your black framed video files inside the video folder.
4. Run the python script.
5. The stripped files will be inside the video folder and have "RED" appended to their file name.


### Params

There's a couple parameters you can tweak. These are located inside the "detect.py" file itself. 

`dur` Set the minimum detected black duration (in seconds)

`pic` Set the threshold for considering a picture as "black" (in percent)

`pix` Set the threshold for considering a pixel "black" (in luminance)


### Contributing

If you find bugs you can notify me by opening an issue. Already solved the bug? Great! Make a pull request and I'll merge it.

#License

Released under the [Apache 2.0 License](https://github.com/code-mc/ffmpegblackframeremove/blob/master/license.md)