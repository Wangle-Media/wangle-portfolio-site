#!/usr/bin/env python3
"""Propose portfolio-grade still frames from a video, as a contact sheet.

Local review tool. It does NOT publish anything: it writes candidate stills and
a numbered contact sheet to a scratch directory so a human can pick, which
matters because the source material here is client work that has not been
cleared for public use.

Selection is deliberately conservative. Most frames in a finished film are bad
stills: mid-motion, mid-transition, mid-dissolve, or a text card. So each
candidate is scored and the weak ones are dropped rather than shown, and the
survivors are spread across the running time so the sheet is not twelve frames
of the same shot.

Usage:
    python tools/pick_frames.py <video> <out_dir> [--every SECONDS] [--top N]
"""
import argparse
import os
import sys

import cv2
import numpy as np


def score(frame):
    """Higher is a better still. Returns (score, reasons_it_might_be_rejected)."""
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sharpness. Motion blur and focus pulls make mush, and mush looks bad
    # blown up on a website.
    sharp = cv2.Laplacian(g, cv2.CV_64F).var()

    # Exposure spread. A frame mid-fade is nearly uniform, and so is a black
    # or white transition, so a tiny standard deviation is a strong reject.
    spread = float(g.std())

    # Colour interest. A flat graphic card scores low; a lit product shot high.
    sat = float(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 1].mean())

    # Text cards tend to be high-contrast edges on a flat ground: lots of edge
    # pixels but very few distinct mid-tones. Penalise that shape.
    edges = cv2.Canny(g, 100, 200)
    edge_ratio = float(edges.mean()) / 255.0
    hist = cv2.calcHist([g], [0], None, [32], [0, 256]).flatten()
    occupancy = float((hist > g.size * 0.002).sum()) / 32.0

    reasons = []
    if spread < 28:
        reasons.append('flat, likely a fade or a plain card')
    if sharp < 55:
        reasons.append('soft, likely motion blur')
    if occupancy < 0.35 and edge_ratio > 0.05:
        reasons.append('reads like a text card')

    s = (min(sharp, 900) / 900.0) * 0.45 + (min(spread, 80) / 80.0) * 0.35 \
        + (min(sat, 140) / 140.0) * 0.20
    return s, reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('out_dir')
    ap.add_argument('--every', type=float, default=2.0, help='sample interval, seconds')
    ap.add_argument('--top', type=int, default=12, help='candidates to keep')
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.video)
    if not cap.isOpened():
        sys.exit('cannot open: %s' % a.video)

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dur = total / fps if fps else 0
    print('%s\n  %dx%d  %.2f fps  %d frames  %.1f s' %
          (os.path.basename(a.video), w, h, fps, total, dur))

    step = max(1, int(round(a.every * fps)))
    cands = []
    for idx in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if not ok:
            continue
        s, reasons = score(frame)
        if reasons:
            continue
        cands.append((s, idx, frame))
    cap.release()
    print('  %d sampled, %d passed the quality gate' % (total // step + 1, len(cands)))
    if not cands:
        sys.exit('  nothing passed; try a smaller --every')

    # Spread the picks over the running time instead of taking the top N, which
    # would cluster on whichever shot happens to be sharpest.
    cands.sort(key=lambda c: c[1])
    buckets = min(a.top, len(cands))
    chosen = []
    for b in range(buckets):
        lo = b * len(cands) // buckets
        hi = max(lo + 1, (b + 1) * len(cands) // buckets)
        chosen.append(max(cands[lo:hi], key=lambda c: c[0]))

    os.makedirs(a.out_dir, exist_ok=True)
    thumbs = []
    for n, (s, idx, frame) in enumerate(chosen, 1):
        t = idx / fps
        name = 'f%02d_%06.2fs.jpg' % (n, t)
        cv2.imwrite(os.path.join(a.out_dir, name),
                    frame, [cv2.IMWRITE_JPEG_QUALITY, 94])
        print('  %2d  %6.2fs  score %.3f  %s' % (n, t, s, name))

        th = cv2.resize(frame, (480, int(480 * h / w)), interpolation=cv2.INTER_AREA)
        cv2.rectangle(th, (0, 0), (78, 26), (0, 0, 0), -1)
        cv2.putText(th, '%02d' % n, (8, 19), cv2.FONT_HERSHEY_SIMPLEX,
                    0.62, (255, 255, 255), 2, cv2.LINE_AA)
        thumbs.append(th)

    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    th_h, th_w = thumbs[0].shape[:2]
    sheet = np.full((rows * th_h, cols * th_w, 3), 24, np.uint8)
    for i, th in enumerate(thumbs):
        r, c = divmod(i, cols)
        sheet[r * th_h:(r + 1) * th_h, c * th_w:(c + 1) * th_w] = th
    sheet_path = os.path.join(a.out_dir, '_contact_sheet.jpg')
    cv2.imwrite(sheet_path, sheet, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print('  contact sheet: %s' % sheet_path)


if __name__ == '__main__':
    main()
