#!/usr/bin/env python3
"""Turn approved source images into the site's case plates.

Centre-crops to the plate's 4:3 aspect and writes a 2x asset so the plate stays
sharp on a high-density screen. Deliberately simple: these are placeholders for
looping animation, so the point is to get them correct and replaceable, not to
build an asset pipeline.

Usage:
    python tools/make_plates.py <src> <out_name> [<src> <out_name> ...]
Writes docs/assets/<out_name>.jpg
"""
import os
import sys

import cv2

W, H = 1280, 720  # 16:9, matching both the plate and every source we have


def crop(img):
    h, w = img.shape[:2]
    target = W / H
    if w / h > target:
        nw = int(h * target)
        img = img[:, (w - nw) // 2:(w - nw) // 2 + nw]
    else:
        nh = int(w / target)
        img = img[(h - nh) // 2:(h - nh) // 2 + nh, :]
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)


def main():
    args = sys.argv[1:]
    if not args or len(args) % 2:
        sys.exit(__doc__)
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'assets')
    os.makedirs(out_dir, exist_ok=True)
    for src, name in zip(args[::2], args[1::2]):
        img = cv2.imread(src, cv2.IMREAD_COLOR)
        if img is None:
            sys.exit('cannot read %s' % src)
        src_h, src_w = img.shape[:2]
        if src_w < W or src_h < H:
            print('  note: %s is %dx%d, below the %dx%d target, upscaling'
                  % (os.path.basename(src), src_w, src_h, W, H))
        out = os.path.join(out_dir, name + '.jpg')
        cv2.imwrite(out, crop(img), [cv2.IMWRITE_JPEG_QUALITY, 84,
                                     cv2.IMWRITE_JPEG_OPTIMIZE, 1])
        print('  %-22s <- %-30s %d KB'
              % (name + '.jpg', os.path.basename(src)[:30],
                 os.path.getsize(out) // 1024))


if __name__ == '__main__':
    main()
