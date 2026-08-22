#!/usr/bin/env python3
"""Measure whether a clip can loop cleanly, and where.

The question "should this loop or ping-pong?" has a measurable answer. A clip
loops cleanly when some later frame closely resembles an early frame, so the cut
back is invisible. When nothing matches, ping-pong (play forward then reverse)
hides the seam instead, at the cost of looking wrong on any motion the eye reads
as directional.

Reports, per clip:
  - duration, resolution
  - whether it opens or closes on black, which is its own kind of clean seam
  - the best loop point found, and how good the match is
  - a recommendation

Usage: python tools/loop_check.py <video> [<video> ...]
"""
import os
import sys

import cv2
import numpy as np


def sig(frame):
    """Small blurred greyscale signature, robust to noise and compression."""
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, (48, 27), interpolation=cv2.INTER_AREA)
    return cv2.GaussianBlur(g, (3, 3), 0).astype(np.float32)


def diff(a, b):
    """Mean absolute difference, 0 = identical, 255 = opposite."""
    return float(np.abs(a - b).mean())


def analyse(path, sample_fps=8.0):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    step = max(1, int(round(fps / sample_fps)))

    sigs, times, brightness = [], [], []
    for idx in range(0, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, fr = cap.read()
        if not ok:
            continue
        sigs.append(sig(fr))
        times.append(idx / fps)
        brightness.append(float(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).mean()))
    cap.release()
    if len(sigs) < 4:
        return None

    # Search for the best (start, end) pair at least 2s apart whose frames match.
    min_gap = max(2, int(2.0 * sample_fps))
    best = None
    for i in range(0, len(sigs) - min_gap):
        for j in range(i + min_gap, len(sigs)):
            d = diff(sigs[i], sigs[j])
            if best is None or d < best[0]:
                best = (d, times[i], times[j])

    return {
        'name': os.path.basename(path), 'w': w, 'h': h, 'fps': fps,
        'dur': total / fps if fps else 0,
        'opens_black': brightness[0] < 12,
        'closes_black': brightness[-1] < 12,
        'best': best,
        'motion': float(np.mean([diff(sigs[k], sigs[k+1]) for k in range(len(sigs)-1)])),
    }


def main():
    for p in sys.argv[1:]:
        r = analyse(p)
        if not r:
            print('%-58s unreadable' % os.path.basename(p)); continue
        d, t0, t1 = r['best']
        print('%s' % r['name'])
        print('   %dx%d  %.2f fps  %.1fs   avg motion %.1f' %
              (r['w'], r['h'], r['fps'], r['dur'], r['motion']))
        print('   opens black: %-5s   closes black: %-5s' %
              (r['opens_black'], r['closes_black']))
        print('   best loop  : %.2fs to %.2fs  (%.1fs long), seam error %.1f' %
              (t0, t1, t1 - t0, d))
        # Thresholds from eyeballing the results against the clips themselves.
        if d < 4:
            verdict = 'LOOP cleanly on that range, seam will be invisible'
        elif r['opens_black'] and r['closes_black']:
            verdict = 'LOOP whole clip, black at both ends hides the cut'
        elif d < 10:
            verdict = 'LOOP acceptable on that range, slight seam'
        else:
            verdict = 'PING-PONG, no clean seam exists'
        print('   -> %s\n' % verdict)


if __name__ == '__main__':
    main()
