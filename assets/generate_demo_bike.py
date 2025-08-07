import cv2
import numpy as np
from pathlib import Path

out_path = Path(__file__).with_name('demo_bike.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 15
size = (320, 240)
writer = cv2.VideoWriter(str(out_path), fourcc, fps, size)

for i in range(fps * 2):  # 2 seconds
    frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    t = i / (fps * 2)
    x = int(40 + t * 80)
    w = int(30 + t * 100)
    h = int(20 + t * 60)
    y = size[1] // 2
    x1 = x
    y1 = y - h // 2
    x2 = x + w
    y2 = y + h // 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)
    writer.write(frame)

writer.release()
print(f"Wrote {out_path}")
