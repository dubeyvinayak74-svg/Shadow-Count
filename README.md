# Shadow-Count

A real-time smart occupancy monitoring system built using YOLO and OpenCV.  
This project detects people, tracks their movement across a defined entry/exit line, and calculates live occupancy. It logs events to CSV and can generate simple visualizations for analysis.

---

## Repository structure
Shadow-Count/
├── code/
│ └── people_counter.py
├── data/
│ └── people_log.csv
├── docs/
│ ├── 30-8-ShadowCount.pdf
│ └── 30-8-ShadowCount(PPT).pptx
├── .gitignore
└── README.md


---

## Installation

This project has already been tested and set up on the developer’s system.  
However, if you want to run it on a new device, follow these installation steps:

### 1️⃣ Install required Python libraries
Use the following command:

```bash
pip install ultralytics opencv-python cvzone matplotlib numpy

