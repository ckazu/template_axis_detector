import argparse
import os
import sys
import cv2
import numpy as np

# parse arguments
parser = argparse.ArgumentParser(description="Detect template image from base image and return it's detected axis.")
parser.add_argument('base_image_path', metavar='BaseImage', type=str, nargs='+', help='base image file path')
parser.add_argument('template_image_path', metavar='TemplateImage', type=str, nargs='+', help='template image file path')
args = parser.parse_args()

# file check
if not(os.path.isfile(args.base_image_path[0])):
    print('error: Could not find `BaseImage` file.')
    sys.exit(1)
if not(os.path.isfile(args.template_image_path[0])):
    print('error: Could not find `TemplateImage` file.')
    sys.exit(1)

# detect images
image = cv2.imread(args.base_image_path[0], 2)
template = cv2.imread(args.template_image_path[0], 2)
w, h = template.shape[::-1]

res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
center = (top_left[0] + w / 2, top_left[1] + h / 2)

sys.stdout.write('{"x":%d,"y":%d}\n' % (round(center[0]), round(center[1])))
