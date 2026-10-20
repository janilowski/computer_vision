# SPDX-FileCopyrightText: 2026 Jan Iłowski
# SPDX-License-Identifier: AGPL-3.0-only

"""Laboratory demo, not robot control. Requires ultralytics, numpy, opencv-python.

No calibration is supplied: default UNKNOWN. --demo-m-per-unit explicitly assumes
registered RGB/depth and metres per raw unit. Neither assumption is verified.
The supplied images show RGB/depth contour offsets.
Depth validity convention: exclude 0 and 65535. FPS is playback speed only.
"""

import argparse
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

HEADER_HEIGHT = 64

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--data", type=Path, default=Path("out_"))
parser.add_argument("--output", default="demo.mp4")
parser.add_argument("--stop-m", type=float, default=1.0)
parser.add_argument("--corridor", type=float, default=0.4, help="Central width fraction")
parser.add_argument("--fps", type=float, default=10, help="Playback FPS, not capture FPS")
parser.add_argument("--demo-m-per-unit", type=float, help="DEMO: assume scale AND registration")
args = parser.parse_args()
if not (0 < args.corridor <= 1 and 0 < args.stop_m < np.inf and 0 < args.fps < np.inf):
    parser.error("Require 0 < corridor <= 1 and positive finite stop-m / fps")
if args.demo_m_per_unit is not None and not 0 < args.demo_m_per_unit < np.inf:
    parser.error("demo-m-per-unit must be positive and finite")

# Pair by numeric ID; mismatches must not silently shift depth to another frame.
rgb_files = {int(p.stem.split("_")[0]): p for p in (args.data / "imgs").glob("*.png")}
depth_files = {int(p.stem.split("_")[0]): p for p in (args.data / "depth16").glob("*.png")}
if not rgb_files or rgb_files.keys() != depth_files.keys():
    parser.error("Require matching numeric IDs in imgs/ and depth16/")

model = YOLO("yolo11n-seg.pt")
writer = None
counts = Counter()
detected_frames = 0
scale = args.demo_m_per_unit
note = "UNKNOWN scale / RGB-depth registration"
if scale is not None:
    note = f"DEMO: ASSUMED alignment + {scale:g} m/raw"
print(note)
print("id,people,state,person_depths_raw")

try:
    for frame_id in sorted(rgb_files):
        rgb = cv2.imread(str(rgb_files[frame_id]))
        depth = cv2.imread(str(depth_files[frame_id]), cv2.IMREAD_UNCHANGED)
        if rgb is None or depth is None or depth.dtype != np.uint16 or depth.shape != rgb.shape[:2]:
            raise ValueError(f"{frame_id}: require RGB and matching single-channel uint16 depth")
        height, width = depth.shape
        left, right = int(width * (1 - args.corridor) / 2), int(width * (1 + args.corridor) / 2)
        if writer is None:
            size = (width, height)
            writer = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*"mp4v"), args.fps, (width, height + HEADER_HEIGHT))
            if not writer.isOpened():
                raise RuntimeError(f"Cannot write {args.output}")
        if (width, height) != size:
            raise ValueError(f"{frame_id}: changing frame size")

        result = model(rgb, classes=[0], retina_masks=True, verbose=False)[0]
        image = result.plot(font_size=10, line_width=1)
        state = "UNKNOWN"
        distances = []
        nearest, unknown = np.inf, False
        if result.masks is not None:
            for mask in result.masks.data.cpu().numpy().astype(bool):
                valid = depth[mask & (depth > 0) & (depth < np.iinfo(np.uint16).max)]
                distance = float(np.median(valid)) if valid.size else np.nan
                distances.append(round(distance, 1))
                if not mask[:, left:right].any():
                    continue
                unknown |= not np.isfinite(distance)
                if np.isfinite(distance):
                    nearest = min(nearest, distance)
            if scale is not None:
                state = "STOP" if nearest * scale < args.stop_m else "UNKNOWN" if unknown else "NO STOP"

        # Only observed masks inform the alarm; a missed person is never proof of clearance.
        detected_frames += bool(distances)
        counts[state] += 1
        color = {"STOP": (0, 0, 255), "UNKNOWN": (0, 200, 255), "NO STOP": (0, 200, 0)}[state]
        cv2.rectangle(image, (left, 0), (right - 1, height - 1), color, 2)
        image = cv2.copyMakeBorder(image, HEADER_HEIGHT, 0, 0, 0, cv2.BORDER_CONSTANT)
        label = f"{state} | {frame_id:04d} | threshold {args.stop_m:g} m"
        cv2.putText(image, label, (5, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.putText(image, note, (5, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        measure = f"{nearest * scale:.2f} m" if scale is not None else f"{nearest:g} raw"
        detail = f"Person depth: {measure}" if np.isfinite(nearest) else "Corridor depth: N/A"
        cv2.putText(image, f"{detail} | detections only", (5, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        writer.write(image)
        print(f"{frame_id:04d},{len(distances)},{state},{distances}")
finally:
    if writer is not None:
        writer.release()

print(f"{args.output}: {len(rgb_files)} frames; detected in {detected_frames}; {dict(counts)}")
