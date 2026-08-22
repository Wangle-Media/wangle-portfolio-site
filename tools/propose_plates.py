#!/usr/bin/env python3
"""Build a single approval sheet showing candidate plate images as they will
actually appear on the site: centre-cropped to the 4:3 plate aspect.

Showing the crop matters. A 16:9 film frame loses a third of its width in a 4:3
plate, and an image that reads well wide can lose its subject entirely once
cropped. Approving the uncropped frame is approving something the visitor never
sees.

Writes to a scratch directory. Publishes nothing.
"""
import os
import sys

import cv2
import numpy as np

PLATE_W, PLATE_H = 640, 360  # 16:9

CANDIDATES = [
    ('02.1  Pandora, conference film', None),
    ('02.2  Pandora, content supply chain', None),
    ('02.3  BRIO, Flora', None),
]


def crop_to_plate(img):
    h, w = img.shape[:2]
    target = PLATE_W / PLATE_H
    if w / h > target:                      # too wide, trim the sides
        new_w = int(h * target)
        x = (w - new_w) // 2
        img = img[:, x:x + new_w]
    else:                                   # too tall, trim top and bottom
        new_h = int(w / target)
        y = (h - new_h) // 2
        img = img[y:y + new_h, :]
    return cv2.resize(img, (PLATE_W, PLATE_H), interpolation=cv2.INTER_AREA)


def label(tile, text, sub):
    cv2.rectangle(tile, (0, PLATE_H - 52), (PLATE_W, PLATE_H), (18, 18, 18), -1)
    cv2.putText(tile, text, (14, PLATE_H - 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.52, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(tile, sub, (14, PLATE_H - 11), cv2.FONT_HERSHEY_SIMPLEX,
                0.42, (170, 170, 180), 1, cv2.LINE_AA)
    return tile


def main():
    paths = sys.argv[1:4]
    out = sys.argv[4]
    if len(paths) != 3:
        sys.exit('need three image paths plus an output path')

    tiles = []
    for (name, _), p in zip(CANDIDATES, paths):
        img = cv2.imread(p, cv2.IMREAD_COLOR)
        if img is None:
            sys.exit('cannot read %s' % p)
        h, w = img.shape[:2]
        tile = crop_to_plate(img)
        tiles.append(label(tile, name, '%s  (source %dx%d)'
                           % (os.path.basename(p)[:38], w, h)))

    gap = 16
    sheet = np.full((PLATE_H + gap * 2, PLATE_W * 3 + gap * 4, 3), 30, np.uint8)
    for i, t in enumerate(tiles):
        x = gap + i * (PLATE_W + gap)
        sheet[gap:gap + PLATE_H, x:x + PLATE_W] = t
    cv2.imwrite(out, sheet, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print('wrote %s' % out)


if __name__ == '__main__':
    main()
