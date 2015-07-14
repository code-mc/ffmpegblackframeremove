# -*- coding: utf-8 -*-
import os, subprocess, time, re

### Options ________________________________________________________________________________________________________
ffmpeg = "ffmpeg.exe"               # Set path to your ffmpeg.exe; 
folder = "videos"                   # Set path to your video folder; 
extensions = [".mov",".mp4"]        # Set which file extensions should be processed
outputAppend = "RED"                # Set the string appended to the processed files
dur = 4                             # Set the minimum detected black duration (in seconds)
pic = 0.98                          # Set the threshold for considering a picture as "black" (in percent)
pix = 0.15                          # Set the threshold for considering a pixel "black" (in luminance)

### Functions ______________________________________________________________________________________________________

def formatTimeString(timeinsec):
    data = str(timeinsec)
    return time.strftime("%H:%M:%S.", time.gmtime(float(data))) + data.split(".")[-1][:3]

def getBlackCuts(filepath):
    sp = subprocess.Popen([ffmpeg, '-i', filepath, '-vf', 
        'blackdetect=d={0}:pic_th={1}:pix_th={2}'.format(str(dur), str(pic), str(pix)), 
        '-an', '-f', 'null', '-', '2>', 'temp'], stdout=subprocess.PIPE, shell=True)
    sp.wait()
    cutlist = []
    startblack = False
    with open("temp", "r+") as f:
        for l in f.read().split("\n"):
            if "black_start:" in l and "black_end:" in l and "black_duration:" in l:
                #print l
                datadict = dict()
                parts = l.split(" ")
                for p in parts:
                    if "black_start:" in p or "black_end:" in p or "black_duration:" in p:
                        data = p.split(":")
                        if data[0] == "black_start" and float(data[1]) < 0.01:
                            startblack = True
                        datadict[data[0]] = formatTimeString(data[1])
                cutlist.append(datadict)
    return (cutlist, startblack)

def cutVideo(video, cutlist, startblack = False):
    output = video.split(".")[0] + "_%03d" + "." + video.split(".")[-1]

    timestring = []
    for d in cutlist:
        timestring.append(d["black_start"])
        timestring.append(d["black_end"])
    timestamps = ",".join(timestring[int(startblack):])
    #print timestamps

    sp = subprocess.Popen([ffmpeg, '-i', video, '-f', 'segment', '-segment_times', timestamps, '-c', 
        'copy', '-map', '0', output, '2>', 'logfile'], stdout=subprocess.PIPE, shell=True)
    sp.wait()

    p = re.compile(video.split(".")[0].split("\\")[-1] + ur'_[0-9]{3}.' + video.split(".")[-1] + '$')
    cuts = []

    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if re.search(p, name):
                cuts.append(os.path.join(root, name))

    cuts = sorted(cuts)
    cutsred = ["file '" + c + "'\n" for i, c in enumerate(cuts) if ((i + int(startblack)) % 2) == 0]
    #print cuts, cutsred
    with open("templist", "w+") as f:
        f.write("\n".join(cutsred))

    sp = subprocess.Popen([ffmpeg, '-f', 'concat', '-i', 'templist', '-c', 'copy', str(outputAppend + ".").join(video.split("."))],
        stdout=subprocess.PIPE, shell=True)
    sp.wait()

    os.remove("templist")
    for c in cuts:
        os.remove(c)

def cleanBlacks():
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if outputAppend not in name and name[-4:] in extensions:
                filepath = os.path.join(root, name)
                cuts = getBlackCuts(filepath)
                cutVideo(filepath, cuts[0], cuts[1])

cleanBlacks()