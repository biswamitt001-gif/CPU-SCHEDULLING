# CPU Scheduling Simulator

A premium, full-stack CPU Scheduling Simulator that visually plots and computes the timelines of fundamental Operating System process scheduling algorithms.

## Features
- **Algorithms Supported:** First Come First Serve (FCFS), Shortest Job First (SJF), Shortest Remaining Time First (SRTF), Priority (Preemptive & Non-Preemptive), and Round Robin (customizable quantum).
- **Glassmorphism UI:** Advanced dark-mode aesthetics utilizing Framer-like micro-animations and interactive particle backgrounds.
- **Accurate Gantt Timelines:** Dynamic, proportional div-based Gantt charts.
- **Performance Analytics:** Chart.js integration for side-by-side Turnaround Time (TAT) and Waiting Time (WT) comparisons.
- **Persistent History:** SQLite-backed simulation history.

## Setup & Running

**Requirements:**
- Python 3.8+

### Quick Start (Windows)
Just double click the `run.bat` file in the root directory. 
It will automatically install requirements and launch the server.

### Manual Start
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Then visit `http://127.0.0.1:5000` in your web browser.

## Technical Details
- **Backend:** Python Flask (`app.py`) providing a RESTful API and static file rendering.
- **Frontend:** Vanilla JavaScript with ES6 features, HTML5, and CSS3 animations.
- **Data Persistence:** Automated `sqlite3` database engine initializing at backend start.
