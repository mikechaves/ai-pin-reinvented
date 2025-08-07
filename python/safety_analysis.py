import sys
import json
import math
import cv2
import torch
import numpy as np
from pathlib import Path

try:
    from moviepy.editor import VideoFileClip
except Exception:
    VideoFileClip = None

def analyze(path):
    video_path = Path(path)
    if not video_path.exists():
        return {"error": f"file not found: {path}"}

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {"error": "cannot open video"}

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, verbose=False)
    relevant = {'bicycle', 'motorcycle'}

    first_det = None
    last_det = None
    last_frame = None
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        detections = []
        for *xyxy, conf, cls in results.xyxy[0].tolist():
            label = model.names[int(cls)]
            if label in relevant:
                x1, y1, x2, y2 = xyxy
                area = (x2 - x1) * (y2 - y1)
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                detections.append({
                    'label': label,
                    'bbox': [x1, y1, x2, y2],
                    'area': area,
                    'cx': cx,
                    'cy': cy,
                    'timestamp': frame_idx / fps,
                    'frame': frame.copy(),
                })
        if detections:
            det = max(detections, key=lambda d: d['area'])
            if first_det is None:
                first_det = det
            last_det = det
            last_frame = det['frame']
        frame_idx += 1

    cap.release()

    danger = False
    direction = None
    eta = None
    suggestion = None
    frame_b64 = None

    if first_det and last_det and last_det['timestamp'] > first_det['timestamp']:
        dt = last_det['timestamp'] - first_det['timestamp']
        area_growth = (last_det['area'] - first_det['area']) / max(first_det['area'], 1) / max(dt, 1e-6)
        center = last_frame.shape[1] / 2.0
        moving_center = abs(last_det['cx'] - center) < abs(first_det['cx'] - center)
        if area_growth > 0.5 and moving_center:
            danger = True
            eta = 1.0 / area_growth if area_growth > 1e-6 else None
            x_center = last_det['cx']
            w = last_frame.shape[1]
            if x_center < w / 3:
                direction = 'left'
                suggestion = 'Move right'
            elif x_center > 2 * w / 3:
                direction = 'right'
                suggestion = 'Move left'
            else:
                direction = 'rear'
                suggestion = 'Speed up'
            # draw box
            x1, y1, x2, y2 = map(int, last_det['bbox'])
            cv2.rectangle(last_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            _, buf = cv2.imencode('.jpg', last_frame)
            frame_b64 = buf.tobytes().hex()

    # optional audio check
    audio_confirm = None
    if VideoFileClip is not None:
        try:
            clip = VideoFileClip(str(video_path))
            audio = clip.audio.to_soundarray(fps=22050)
            if len(audio) > 0:
                n = len(audio)
                first = audio[:n // 3]
                last = audio[-n // 3:]
                rms1 = np.sqrt(np.mean(first**2))
                rms2 = np.sqrt(np.mean(last**2))
                audio_confirm = rms2 > rms1 * 1.3
            clip.close()
        except Exception:
            audio_confirm = None

    return {
        'danger': danger,
        'direction': direction,
        'eta_sec': eta,
        'suggestion': suggestion,
        'audio_increase': audio_confirm,
        'frame': frame_b64,
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: python safety_analysis.py <path>"}))
        sys.exit(0)
    result = analyze(sys.argv[1])
    print(json.dumps(result))
