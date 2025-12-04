import cv2
from ultralytics import YOLO
import cvzone
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict

# ============================
# YOLO SETUP
# ============================

model = YOLO("yolo12n.pt")
names = model.names

line_x = 620
track_history = {}

in_count = 0
out_count = 0

MAX_CAPACITY = 20

# Use "0" for webcam instead of a video file
cap = cv2.VideoCapture("LRC.mp4")  # change to 0 for webcam

# Mouse callback
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Mouse moved to: [{x}, {y}]")

cv2.namedWindow("RGB")
cv2.setMouseCallback("RGB", RGB)

# ============================
# CSV FILE CREATION
# ============================

CSV_FILE = "people_log.csv"

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "person_id", "direction", "inside_count"])

# ============================
# LIVE PEOPLE COUNTER
# ============================

# --- add near the top, after track_history definition ---
highlight = {}                # track_id -> remaining frames to show green
HIGHLIGHT_FRAMES = 25         # number of frames to keep green highlight after an event

# ... rest of your setup ...

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 2 != 0:
        continue  # skip every alternate frame

    frame = cv2.resize(frame, (1020, 600))

    results = model.track(frame, persist=True, classes=[0])  # class 0 = person

    # decrement highlight timers
    for tid in list(highlight.keys()):
        highlight[tid] -= 1
        if highlight[tid] <= 0:
            del highlight[tid]

    if results and len(results) > 0 and results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

        for track_id, box in zip(ids, boxes):
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) // 2)
            cy = int((y1 + y2) // 2)

            # default box color (B, G, R)
            box_color = (255, 0, 0)  # blue by default

            if track_id in track_history:
                prev_cx, prev_cy = track_history[track_id]

                # ENTER (crossing left -> right)
                if prev_cx < line_x <= cx:
                    in_count += 1

                    inside_event = in_count - out_count
                    if inside_event < 0:
                        inside_event = 0

                    # Log IN
                    with open(CSV_FILE, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            int(track_id),
                            "IN",
                            inside_event
                        ])

                    # set highlight for this id
                    highlight[track_id] = HIGHLIGHT_FRAMES
                    box_color = (0, 255, 0)  # green on event

                # EXIT (crossing right -> left)
                if prev_cx > line_x >= cx:
                    out_count += 1

                    inside_event = in_count - out_count
                    if inside_event < 0:
                        inside_event = 0

                    # Log OUT
                    with open(CSV_FILE, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            int(track_id),
                            "OUT",
                            inside_event
                        ])

                    # set highlight for this id
                    highlight[track_id] = HIGHLIGHT_FRAMES
                    box_color = (0, 255, 0)  # green on event

            # If the id has a remaining highlight timer, use green
            if track_id in highlight:
                box_color = (0, 255, 0)

            # Draw bounding box and centroid
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.circle(frame, (cx, cy), 4, box_color, -1)
            cvzone.putTextRect(frame, f'ID: {int(track_id)}', (x1, y1 - 10), 1, 1, colorR=(box_color[2], box_color[1], box_color[0]))

            # update history
            track_history[track_id] = (cx, cy)

    # DISPLAY COUNTS (same as before)
    inside = in_count - out_count
    if inside < 0:
        inside = 0

    remaining = MAX_CAPACITY - inside
    if remaining < 0:
        remaining = 0

    cvzone.putTextRect(frame, f'IN: {in_count}', (40, 60), 2, 2, colorR=(0, 128, 0))
    cvzone.putTextRect(frame, f'OUT: {out_count}', (40, 100), 2, 2, colorR=(0, 0, 255))
    cvzone.putTextRect(frame, f'INSIDE: {inside}', (40, 140), 2, 2, colorR=(128, 0, 128))
    cvzone.putTextRect(frame, f'SPACE LEFT: {remaining}', (40, 180), 2, 2, colorR=(0, 128, 128))

    cv2.line(frame, (line_x, 0), (line_x, frame.shape[0]), (255, 255, 255), 2)

    cv2.imshow("RGB", frame)

    # ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ============================
# GENERATE GRAPHS AUTOMATICALLY
# ============================

timestamps = []
inside_counts = []
entries_per_interval = defaultdict(int)

start_time = None

# Read CSV
with open(CSV_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
        inside_val = int(row["inside_count"])
        if inside_val < 0:
            inside_val = 0

        timestamps.append(ts)
        inside_counts.append(inside_val)

        if start_time is None:
            start_time = ts  # first timestamp

        # For 10-second interval entries (only IN events)
        if row["direction"] == "IN":
            seconds_from_start = (ts - start_time).total_seconds()
            interval_index = int(seconds_from_start // 10)  # 0–10, 10–20, ...
            entries_per_interval[interval_index] += 1

# If no data, skip plotting
if not timestamps:
    print("No data in CSV to plot.")
else:
    # ===== MERGED FIGURE WITH TWO GRAPHS =====
    if entries_per_interval:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(10, 5))
        ax2 = None

    # GRAPH 1 - INSIDE COUNT VS TIME
    ax1.plot(timestamps, inside_counts, marker="o")
    ax1.set_title("People Inside vs Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Inside Count")
    ax1.grid(True)
    fig.autofmt_xdate()

    # GRAPH 2 - ENTRIES PER 10-SECOND TIMESTAMP INTERVAL
    if entries_per_interval and ax2 is not None:
        intervals = sorted(entries_per_interval.keys())
        counts = [entries_per_interval[i] for i in intervals]

        labels = []
        for i in intervals:
            t1 = start_time + timedelta(seconds=i * 10)
            t2 = start_time + timedelta(seconds=(i + 1) * 10)
            labels.append(f"{t1.strftime('%H:%M:%S')} - {t2.strftime('%H:%M:%S')}")

        ax2.bar(range(len(labels)), counts)
        ax2.set_title("Entries per 10-Second Interval")
        ax2.set_xlabel("Timestamp Range")
        ax2.set_ylabel("Number of Entries")
        ax2.set_xticks(range(len(labels)))
        ax2.set_xticklabels(labels, rotation=45, ha="right")

    plt.tight_layout()
    plt.show()
