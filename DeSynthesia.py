import cv2
import numpy as np
from matplotlib import pyplot as plt
import NoteDicts
import sys
import time
from midiutil.MidiFile import MIDIFile
from note import Note


y = 600
flatoffset = 9
naturaloffset = 12
saturationthresh = 120 # saturation required for a note to be considered a note
video_name = "christmas.mp4"
output_name = "output.mp4"
tempo = 90 #bpm
seconds_to_skip_at_start = 3

start = time.time() # time used for progress bar
cap = cv2.VideoCapture(video_name)
fps = cap.get(cv2.CAP_PROP_FPS)
skipframes = seconds_to_skip_at_start * fps

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
insize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (insize[0], insize[1]))
mf = MIDIFile(1)
track = 0
timeidk = 0
mf.addTrackName(track, timeidk, "Track 1")
mf.addTempo(track, timeidk, tempo)
channel = 0
volume = 100

current_set = {}
last_set = {}

def color_at_both_points(x1, x2, hsv):
    saturation1 = hsv[y, x1][1]
    saturation2 = hsv[y, x2][1]
    if saturation1 > saturationthresh and saturation2 > saturationthresh:
        #print(f"Saturation 1: {saturation1}, Saturation 2: {saturation2}")
        return True
    return False

def progress(purpose,currentcount, maxcount):
    timeelapsed = round(time.time() - start)
    sys.stdout.write('\r')
    sys.stdout.write("{}: {:.1f}%, {} of {}, {} seconds elapsed".format(purpose, (100/(maxcount-1)*currentcount),
                                                                        currentcount, maxcount, timeelapsed))
    sys.stdout.flush()


notes = NoteDicts.getnotes()
midi = NoteDicts.getmidi()

counter = 0
while cap.isOpened():
    currentnotes = []
    ret, frame = cap.read()
    if not ret:
        break
    if counter < skipframes:
        counter += 1
        continue
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for note in notes:
        x = notes[note]
        if "flat" in note:
            x1 = x + flatoffset
            x2 = x - flatoffset
            text_y = y + 100
        else:
            x1 = x + naturaloffset
            x2 = x - naturaloffset
            text_y = y + 200
        if color_at_both_points(x1, x2, hsv):
            currentnotes.append(note)
    for note in currentnotes:
        try:
            note_object = last_set[note]
            # In current notes and last notes, this is a continuing note, update its end time
            note_object.set_end_time(counter/fps)
            current_set[note] = note_object
        except KeyError:
            # In current notes but not last notes, this is a new note
            current_set[note] = Note(note, counter/fps)

    # if any notes are in the past_set that aren't in the current_set, they are an ended note, add them to the midi
    for key in last_set:
        try:
            note = current_set[key]
        except KeyError:
            last_note_object = last_set[key]
            pitch = midi[key]
            mf.addNote(track, channel, pitch, last_note_object.get_start_time(), last_note_object.get_duration(), volume)
            print(f"note: {key}, start time: {last_note_object.get_start_time()}, duration: {last_note_object.get_duration()}")
            #print(last_note_object)

    # finally, replace the last set with the current set
    last_set = current_set
    current_set = {}

    #print(currentnotes)
    out.write(frame)
    # progress("Frames analyzed", counter, frame_count)
    # scale_percent = 50# percent of original size
    # width = int(frame.shape[1] * scale_percent / 100)
    # height = int(frame.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    counter += 1


cap.release()
print("\nDone")

with open("output.mid", 'wb') as outfile:
    mf.writeFile(outfile)