# This script lets you test the placement of the notes using the video. On alternating frames, lines will be drawn for
# black and white notes. The note separations can be adjusted in NotePixel.py. This adjustment would optimally be done
# with a gui, where you can drag the bars and see how the notes fit onto the piano, but this is not a high priority.

import cv2
import dicts
import random

y = 600
flatoffset = 8
naturaloffset = 12

video_name = "christmas.mp4"

cap = cv2.VideoCapture(video_name)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
insize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))



def color_at_both_points(x1, x2, frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    saturation1 = hsv[y, x1][1]
    saturation2 = hsv[y, x2][1]
    if saturation1 > 40 and saturation2 > 40:
        print(f"Saturation 1: {saturation1}, Saturation 2: {saturation2}")
        return True
    return False


# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
#
# cv2.resizeWindow('image', in_size[0], in_size[1])

notes = dicts.get_notes()


counter = 0
while cap.isOpened():
    ret, frame = cap.read()
    scale_percent = 50# percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    for note in notes:
        x = notes[note]
        # print(len(notes))
        tint = random.randint(0,255)
        if "flat" in note:
            color = (tint, 255,255-tint)
            offset = 8
        else:
            color = (tint, 255-tint, 255)
            offset = 12
        if "flat" in note and counter % 2 == 1 or "flat" not in note and counter % 2 == 0:
            frame = cv2.line(frame, (x+offset, y-10), (x+offset, y+10),color, 1)
            frame = cv2.line(frame, (x-offset, y-10), (x-offset, y+10), color, 1)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('image', frame)
    cv2.waitKey()
    counter += 1

