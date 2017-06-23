import argparse
import os
import sys
import cv2
import numpy as np

# parse arguments
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % (x,))
    return x

parser = argparse.ArgumentParser(description="Detect template image from base image and return it's detected axis.")
parser.add_argument('base_image_path', metavar='BaseImage', type=str, nargs='+', help="read base image file")
parser.add_argument('template_image_path', metavar='TemplateImage', type=str, nargs='+', help="read template image file")
parser.add_argument('--matching-accuracy', metavar='Accuracy', type=restricted_float, default=0.8, help='set the matching accuracy (default: 0.8)')
parser.add_argument('-o', '--output', metavar='OutputImage', type=str, help='output result as composite image')

args = parser.parse_args()

# file check
if not(os.path.isfile(args.base_image_path[0])):
    sys.stderr.write('error: Could not find `BaseImage` file.\n')
    sys.exit(1)
if not(os.path.isfile(args.template_image_path[0])):
    sys.stderr.write('error: Could not find `TemplateImage` file.\n')
    sys.exit(1)

# detect images
image = cv2.imread(args.base_image_path[0], 2)
template = cv2.imread(args.template_image_path[0], 2)
w, h = template.shape[::-1]

res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

if max_val < args.matching_accuracy:
    sys.stdout.write('{"matched":false,"max-accuracy":%f}\n' % max_val)
    sys.exit(0)

top_left = max_loc
center = (top_left[0] + w / 2, top_left[1] + h / 2)

sys.stdout.write('{"matched":true,"x":%d,"y":%d,"accuracy":%f}\n' % (round(center[0]), round(center[1]), max_val))

if args.output:
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    cv2.imwrite(args.output, image)
