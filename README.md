# 🔥 Shadow-Count — Smart Occupancy Monitoring System

Shadow-Count is an intelligent real-time people tracking and occupancy monitoring system built using **YOLO** 🧠 and **OpenCV** 🎥.  
It detects people, tracks them across an entry/exit line, and calculates the live occupancy inside any space — cleanly and accurately.

---

## ⚙️ How It Works (Short & Simple)

1️⃣ **Detect People** – YOLO identifies each person in the camera frame.  
2️⃣ **Track Movement** – The system assigns unique IDs and follows each person.  
3️⃣ **Line Crossing Logic** – When a person crosses the virtual line ➝ IN or OUT is counted.  
4️⃣ **Live Occupancy Update** – Inside count is updated in real time & logged into CSV.  

---

## 📁 Repository Structure
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

## 🛠 Installation (Quick)

Install the required Python libraries:

```bash
pip install ultralytics opencv-python cvzone matplotlib numpy
```



Place the YOLO model file (yolo12n.pt) in the same folder as the Python script while running locally.

🚀 Run the Project

From the repository root, run:

cd code
python shadowcount.py

📊 Output Features

✨ Live IN / OUT Counting
✨ Real-time Occupancy Display
✨ CSV Logging for Analytics
✨ Graphs for time-based activity (optional)


---

## 👥 Team Details

### 🏷 Team Name: **Shadow-Count**

### 👨‍💻 Team Members & Contributions

| Name | Role / Contribution |
|------|----------------------|
| **Harsh Ahlawat** | Lead Developer — YOLO model integration, core logic, and system pipeline implementation |
| **Vinayak Dubey** | Testing Engineer — Camera testing (Webcam, DroidCam), video-based evaluation, deployment optimization |
| **Md Rahbar Anwar** | Documentation & Research — System workflow documentation, research on occupancy monitoring concepts |
| **Himanshu Yadav** | Presentation & Applications — PPT design, application use-cases, report structuring |

---




