import os
import pandas as pd

def read_bvh(filename):
    file = open(filename, "r", encoding="utf-8")
    bvh_text  = file.readlines()
    file.close()
    i=1
    skeleton = []
    frames=[]
    while bvh_text[i].strip().upper() != "MOTION":
        if bvh_text[i].strip() !="":
            skeleton.append(bvh_text[i])
        i+=1
    while not bvh_text[i].strip().upper().startswith("FRAME TIME"):
        i+=1
    frame_time = bvh_text[i].split()[2]
    i+=1
    while i < len(bvh_text):
        frames.append(bvh_text[i].strip())
        i+=1
    return "".join(skeleton).rstrip(), frame_time, frames

def write_bvh(filepath, filename, skeleton, frame_time, frames):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    outfile = "%s%s%s" % (filepath, os.path.sep, filename)
    f = open(outfile,"w", encoding="utf-8")
    f.write("HIERARCHY\n")
    f.write("%s\n" % (skeleton))
    f.write("MOTION\n")
    f.write("Frames: %d\n" % (len(frames)))
    f.write("Frame Time: %s\n" % (frame_time))
    for frame in frames:
        f.write("%s\n" % (frame))
    f.close()

csvfile = "..%sCMU data.csv" % (os.path.sep)
data = pd.read_csv(csvfile, encoding="utf-8")

# Verifiy all the AMC files exist
source = "CMU ASF AMC%ssubjects" % os.path.sep
for i, j in data.iterrows():
    subject = j['Subject']
    trial = j['Trial #']
    desc =j['Motion Description']
    filename = "%s%s%02d%s%02d_%02d.amc" % (source, os.path.sep,subject, os.path.sep,subject, trial)
    if not os.path.exists(filename):
        print(filename, os.path.exists(filename))

# Verifiy all the BVH files exist
source = "CMU_BVH%ssubjects" % os.path.sep
for i, j in data.iterrows():
    subject = j['Subject']
    trial = j['Trial #']
    desc =j['Motion Description']
    filename = "%s%s%02d%s%02d_%02d.bvh" % (source, os.path.sep,subject, os.path.sep,subject, trial)
    if not os.path.exists(filename):
        print(filename, os.path.exists(filename))

# FIXME: Do this by looping through dataframe
for i, j in data.iterrows():
    pass
    subject = j['Subject']
    trial = j['Trial #']
    desc =j['Motion Description']
    framerate = j['framerate']

    filename = "%s%s%02d%s%02d_%02d.bvh" % (source, os.path.sep,subject, os.path.sep,subject, trial)
    tfile = "%s%s%02d%s%02d.bvh" % (source, os.path.sep,subject, os.path.sep,subject)
    if not os.path.exists(tfile):
        exit()

    skel, ft, f=read_bvh(filename)
    tskel, tft,tf =read_bvh(tfile)

    # Prepend T-Pose
    f.insert(0,tf[0])

    # Set the frame rate to the correct one
    if framerate == 120:
        ft="0.008333"
        tft="0.008333"
    elif framerate == 60:
        tft="0.016667"
        tft="0.016667"

    # Write out the file
    dest = "CMU_BVH_OT%ssubjects" % os.path.sep
    destpath="%s%s%03d" % (dest,os.path.sep, subject)
    destfile = "%03d_%02d.bvh" % (subject,trial)
    #dest_t ="%03d.bvh" % (subject)
    write_bvh(destpath,destfile,skel,ft,f)

    print(framerate, "%s%s%s" % (destpath,os.path.sep, destfile))
