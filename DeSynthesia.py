# Author: Kevin Lin
# Date: 7/30/2021
# Description: Script for reading a Synthesia-esque piano tutorial and converting to a MIDI file that another program, namely
# MuseScore, can translate to sheet music. This is an updated version that focuses on SheetMusicBoss because their videos
# are more vulnerable

import math
import cv2

import dicts
import sys
import time
from midiutil.MidiFile import MIDIFile
from note import Note

mode = dicts.SheetMusicBoss
saturation_thresh = 120 # saturation required for a note to be considered a note
rounding = True # turn off for swingy songs
rounding_quanta = 32 # what 'th note to round to
video_name = "rasputin.mp4"
output_name = "output.mp4"
output_midi_name = f"output{rounding_quanta}.mid"
tempo = 124 #bpm
seconds_to_skip_at_start = 3
seconds_to_skip_at_end = 18

debug = False
start = time.time() # time used for progress bar
cap = cv2.VideoCapture("input_videos/" + video_name)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
skip_frames_start = seconds_to_skip_at_start * fps
skip_frames_end = frame_count - seconds_to_skip_at_end * fps

in_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(output_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (in_size[0], in_size[1]))
mf = MIDIFile(2)
track = 0
track2 = 1
midi_time = 0
mf.addTrackName(track, midi_time, "Right Hand")
mf.addTrackName(track2, midi_time, "Left Hand")
mf.addTempo(track, midi_time, tempo)
mf.addTempo(track2, midi_time, tempo)
channel = 0
volume = 100
notes = dicts.get_notes(dicts.SheetMusicBoss)
midi = dicts.getmidi()


def color_at_point(x, y, hsv):
    saturation = hsv[y, x][1]
    if saturation > saturation_thresh:
        #print(f"Saturation 1: {saturation1}, Saturation 2: {saturation2}")
        return True
    return False


def right_or_left(x, y, frame):
    bgr = frame[y,x]
    blue = bgr[0]
    green = bgr[1]
    # right hand is green notes, left hand is blue notes, this will change if generalizing
    if blue < green:
        return "right"
    else:
        return "left"


def progress(purpose,current_count, max_count):
    timeelapsed = round(time.time() - start)
    sys.stdout.write('\r')
    sys.stdout.write("{}: {:.1f}%, {} of {}, {} seconds elapsed".format(purpose, (100/(max_count-1)*current_count),
                                                                        current_count, max_count, timeelapsed))
    sys.stdout.flush()


def desynthesize():
    current_set = {}
    last_set = {}
    counter = 0
    current_track = 0
    while cap.isOpened():
        found_notes = []
        ret, frame = cap.read()
        if not ret:
            break
        if counter < skip_frames_start or counter > skip_frames_end:
            counter += 1
            continue
        if rounding:
            current_time_in_beats = math.floor(counter / fps * tempo / 60 * rounding_quanta) / rounding_quanta
        else:
            current_time_in_beats = counter / fps * tempo / 60
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for note in notes:
            x = notes[note]
            if "flat" in note:
                text_y = 909
            else:
                text_y = 1036
            if color_at_point(x, text_y, hsv):
                color = right_or_left(x, text_y, frame)
                if color == "right":
                    circle_color = (0, 255, 0)
                    current_track = "right"
                elif color == "left":
                    circle_color = (255, 0, 0)
                    current_track = "left"
                else:
                    circle_color = (255, 255, 255)
                cv2.circle(frame, (x,text_y), 7, circle_color, -1)
                found_notes.append(note)
                try:
                    note_object = last_set[note]
                    # In current notes and last notes, this is a continuing note, update its end time
                    note_object.set_end_time(current_time_in_beats)
                    current_set[note] = note_object
                except KeyError:
                    # In current notes but not last notes, this is a new note
                    current_set[note] = Note(note, current_time_in_beats, current_track)
        if debug:
            #plt.imshow(frame)
            #plt.show()
            scale_percent = 50# percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow("Testing placement of notes", frame)
            cv2.waitKey(0)
            continue

        # if any notes are in the past_set that aren't in the current_set, they are an ended note, add them to the midi
        for key in last_set:
            try:
                note = current_set[key]
            except KeyError:
                last_note_object = last_set[key]
                pitch = midi[key]
                start_time = last_note_object.get_start_time()
                duration = last_note_object.get_duration()
                track = 0 if last_note_object.get_hand() == "right" else 1
                if duration < 0.01:
                    # no zero durations
                    duration = 0.01

                mf.addNote(track, channel, pitch, start_time, duration, volume)
                print(f"note: {key}, start time: {start_time}, duration: {duration}, track: {track}")
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
    print(f"\nDone. You can convert {output_midi_name} to sheet music using MuseScore now")

    with open(output_midi_name, 'wb') as outfile:
        mf.writeFile(outfile)


if __name__ == "__main__":
    desynthesize()
