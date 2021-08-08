# Author: Kevin Lin
# Date: 7/30/2021
# Description: Script for reading a Synthesia-esque piano tutorial and converting to a MIDI file that another program, namely
# MuseScore, can translate to sheet music.

import math
import cv2
import numpy as np
from matplotlib import pyplot as plt
import dicts
import sys
import time
from midiutil.MidiFile import MIDIFile
from note import Note


y = 600
flat_offset = 9
natural_offset = 12
saturation_thresh = 120 # saturation required for a note to be considered a note
video_name = "christmas.mp4"
output_name = "output.mp4"
output_midi_name = "tables.mid"
tempo = 70 #bpm
seconds_to_skip_at_start = 3
rounding = False # turn off for swingy songs

start = time.time() # time used for progress bar
cap = cv2.VideoCapture(video_name)
fps = cap.get(cv2.CAP_PROP_FPS)
skip_frames = seconds_to_skip_at_start * fps

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
in_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (in_size[0], in_size[1]))
mf = MIDIFile(1)
track = 0
midi_time = 0
mf.addTrackName(track, midi_time, "Track 1")
mf.addTempo(track, midi_time, tempo)
channel = 0
volume = 100
notes = dicts.get_notes()
midi = dicts.getmidi()


def color_at_both_points(x1, x2, hsv):
    saturation1 = hsv[y, x1][1]
    saturation2 = hsv[y, x2][1]
    if saturation1 > saturation_thresh and saturation2 > saturation_thresh:
        #print(f"Saturation 1: {saturation1}, Saturation 2: {saturation2}")
        return True
    return False


def progress(purpose,currentcount, maxcount):
    timeelapsed = round(time.time() - start)
    sys.stdout.write('\r')
    sys.stdout.write("{}: {:.1f}%, {} of {}, {} seconds elapsed".format(purpose, (100/(maxcount-1)*currentcount),
                                                                        currentcount, maxcount, timeelapsed))
    sys.stdout.flush()



def desynthesize():
    current_set = {}
    last_set = {}
    counter = 0
    while cap.isOpened():
        found_notes = []
        ret, frame = cap.read()
        if not ret:
            break
        if counter < skip_frames:
            counter += 1
            continue
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for note in notes:
            x = notes[note]
            if "flat" in note:
                x1 = x + flat_offset
                x2 = x - flat_offset
                text_y = y + 100
            else:
                x1 = x + natural_offset
                x2 = x - natural_offset
                text_y = y + 200
            if color_at_both_points(x1, x2, hsv):
                found_notes.append(note)

        for note in found_notes:
            if rounding:
                current_time_in_beats = math.floor(counter / fps * tempo / 60 * 16) / 16 # rounding to nearest 16th note
            else:
                current_time_in_beats = counter / fps * tempo / 60
            try:
                note_object = last_set[note]
                # In current notes and last notes, this is a continuing note, update its end time
                note_object.set_end_time(current_time_in_beats)
                current_set[note] = note_object
            except KeyError:
                # In current notes but not last notes, this is a new note
                current_set[note] = Note(note, current_time_in_beats)

        # if any notes are in the past_set that aren't in the current_set, they are an ended note, add them to the midi
        for key in last_set:
            try:
                note = current_set[key]
            except KeyError:
                last_note_object = last_set[key]
                pitch = midi[key]
                start_time = last_note_object.get_start_time()
                duration = last_note_object.get_duration()
                if duration < 0.01:
                    # no zero durations
                    duration = 0.01
                mf.addNote(track, channel, pitch, start_time, duration, volume)
                print(f"note: {key}, start time: {start_time}, duration: {duration}")
                #print(last_note_object)

        # finally, replace the last set with the current set
        last_set = current_set
        current_set = {}

        #print(found_notes)
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

    with open(output_midi_name, 'wb') as outfile:
        mf.writeFile(outfile)


if __name__ == "__main__":
    desynthesize()