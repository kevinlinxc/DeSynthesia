import easygui
import os
from pdf2image import convert_from_path
import shutil
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
import math

track_title = "Use this window to crop the sides of a row of measures. Select the row and hit any key to finish with that row."
left = None
right = None
current_image = None
buffer = 10
output_name = "output90.png"

def wipe_directory(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        try:
            shutil.rmtree(filepath)
        except OSError:
            os.remove(filepath)


def open_image(path):
    image = Image.open(path) #open in grayscale mode 'L'
    image = image.convert('L')
    return np.array(image)


def line_contrast(page_image):
    line_contr =[]
    for line in page_image: #determine range per line
        line_contr.append(max(line) - min(line))
    return line_contr


def find_rows(line_contr):
    detected_rows = []
    row_start = 0
    row_end = 0
    detect_state = 0 #0 if previous line was not part of a row
    cur_row = 0
    for contrast in line_contr:
        if contrast < 50 and detect_state == 0:
            row_start = cur_row
        elif contrast >= 50 and detect_state == 0:
            row_start = cur_row
            detect_state = 1
        elif contrast < 50 and detect_state == 1: #if end of row, evaluate AOI height
            row_end = cur_row
            rowheight = row_start - row_end
            if abs(rowheight) >= 150:
                detected_rows.append((row_start, row_end))
            detect_state = 0
        elif contrast >= 50 and detect_state == 1:
            pass
        else:
            print("unknown situation, help!, detection state: " + str(detect_state))
        cur_row += 1
    return detected_rows


def on_trackbar(var):
    global left
    global right
    left = cv2.getTrackbarPos("left", track_title)
    right = cv2.getTrackbarPos("right", track_title)
    cv2.imshow("current_image", current_image[top:bottom, left:right])


# Go get pdf that needs to be cut up
file_path = easygui.fileopenbox()
base = os.path.basename(file_path)
file_name = os.path.splitext(base)[0]
# poppler is a pdf software that pdf2image wraps around.
poppler_version = "poppler-21.08.0"
poppler_path = os.path.join(os.getcwd(), poppler_version, "Library", "bin")
# print(f"Path to poppler: {poppler_path}")

pages = convert_from_path(file_path, poppler_path=poppler_path)
temp_path = os.path.join(os.curdir, "flatten", "temp")
# print(temp_path)
wipe_directory(temp_path)

saved_rows = []
num_pages = len(pages)

for index, page in enumerate(pages):
    page_name = f"{index} - {file_name}.jpg"
    page.save(f"{os.path.join(temp_path, page_name)}", format="jpeg")


for i in range(num_pages):
    page_name = f"{i} - {file_name}.jpg"
    image_path = os.path.join(temp_path, page_name)
    img = open_image(os.path.join(os.getcwd(), image_path))
    img_copy = img.copy()
    print(img.shape)
    height = img.shape[0]
    line_contr = line_contrast(img)
    detected_rows = find_rows(line_contr)
    for row_index, row in enumerate(detected_rows):
        if row[0] - buffer < 0:
            top = 0
        else:
            top = row[0] - buffer

        if row[1] + buffer > height:
            bottom = height
        else:
            bottom = row[1] + buffer
        cv2.namedWindow(track_title)
        cv2.resizeWindow(track_title, 1000, 240)
        staff_row = img[top:bottom, :]
        rightmost = img.shape[1]
        current_image = img
        cv2.imshow(f"current_image", staff_row)
        track_left_start = left if left else 0
        track_right_start = right if right else rightmost

        cv2.createTrackbar("left", track_title, track_left_start, rightmost, on_trackbar)
        cv2.createTrackbar("right", track_title, track_right_start, rightmost, on_trackbar)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        img[row[0], left:right] = 0
        img[row[1], left:right] = 0
        img[row[0]:row[1], left] = 0
        img[row[0]:row[1], right-1] = 0

        print(f"top: {top}, bottom: {bottom}, left: {left}, right: {right} for line {row_index} for page {i}")
        saved_rows.append(img_copy[top:bottom, left:right])
    plt.rcParams["keymap.quit"] = ['ctrl+w', 'cmd+w', 'q', 'space']
    show = plt.imshow(img, cmap='gray')
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()

cv2.destroyAllWindows()
max_height = 0
for row in saved_rows:
    height = row.shape[0]
    max_height = max(height, max_height)
    # cv2.imshow("Results", row)
    # cv2.waitKey(0)
print(f"Max height: {max_height}")

final_array = np.ones((max_height, 1)) * 255
for i in range(len(saved_rows)):
    row_height = saved_rows[i].shape[0]
    height_diff = max_height - row_height
    bot_padding = math.ceil(height_diff/2)
    top_padding = math.floor(height_diff/2)
    padded = cv2.copyMakeBorder(saved_rows[i], top_padding, bot_padding, 0, 0, cv2.BORDER_CONSTANT, value=[255])
    final_array = np.hstack([final_array, padded])

img_rotate_90_clockwise = cv2.rotate(final_array, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite(output_name, img_rotate_90_clockwise)


print(f"Saved rows to {output_name}")