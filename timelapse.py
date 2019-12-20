# Creates a timelapse video from a folder of images
import glob
import os

import cv2
from time import time

TIMELAPSE_RESOLUTION = (1920, 1080)
fps = 30
duration = 100
video_filename = os.path.join('timelapse', 'timelapse_{}.avi'.format(int(time())))

source_path = input('Source directory: ')

image_frames = glob.glob(os.path.join(source_path, '*.jpg'))
image_frames.sort()

img1 = cv2.imread(image_frames[0])
frame = cv2.resize(img1, TIMELAPSE_RESOLUTION, fx=0, fy=0, interpolation=cv2.INTER_AREA)
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

start = time()
total_images = len(image_frames)
image_count = 0
print('Start making video with ' + str(total_images) + ' images')

# Write frames to video
for i in range(total_images):
    image_count = i
    img = cv2.imread(image_frames[i])
    frame = cv2.resize(img, (width, height), fx=0, fy=0, interpolation=cv2.INTER_AREA)
    for _ in range(int(fps * duration / 1000)):
        out.write(frame)
    print('Progress: ' + str((i + 1)/total_images * 100) + '%')

# Add a pause at the end with the last frame
img = cv2.imread(image_frames[-1])
frame = cv2.resize(img, (width, height), fx=0, fy=0, interpolation=cv2.INTER_AREA)

# Last frame lasts an additional (last_frame_duration * self.duration / 1000) ms
# When last_frame_duration = 10 and self.duration = 100, last frame will stay for 1 second
last_frame_duration = 10
for _ in range(int(fps * last_frame_duration * duration / 1000)):
    out.write(frame)

out.release()

print('Finished writing video with ' + str(image_count + 1) + '/' +
      str(total_images) + ' images, took ' + str(time() - start) + 's')
