"""
CPU Scheduling Simulator — Flask Backend
Serves the REST API at /schedule and static frontend files.
"""
import os
import sys

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Ensure backend package is on path
sys.path.insert(0, os.path.dirname(__file__))

from algorithms import fcfs, sjf, srtf, priority, round_robin
import db

# ─────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

db.init_db()


# ─────────────────────────────────────────────
# Serve frontend
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)


# ─────────────────────────────────────────────
# /schedule  POST
# ─────────────────────────────────────────────
@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json(silent=True)

    # ── Input validation ──────────────────────
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    algorithm = data.get("algorithm", "").strip().upper()
    processes = data.get("processes", [])
    quantum = data.get("quantum", 2)

    if not algorithm:
        return jsonify({"error": "Field 'algorithm' is required."}), 400

    valid_algorithms = {"FCFS", "SJF", "SRTF", "PRIORITY", "PRIORITY_P", "RR"}
    if algorithm not in valid_algorithms:
        return jsonify({
            "error": f"Unknown algorithm '{algorithm}'. Valid options: {sorted(valid_algorithms)}"
        }), 400

    if not isinstance(processes, list) or len(processes) == 0:
        return jsonify({"error": "Field 'processes' must be a non-empty list."}), 400

    # Validate and normalise each process
    normalised = []
    for i, p in enumerate(processes):
        try:
            pid = str(p.get("id", f"P{i+1}")).strip()
            arrival = int(p["arrival"])
            burst = int(p["burst"])
            prio = int(p.get("priority", 1))
        except (KeyError, ValueError, TypeError) as e:
            return jsonify({"error": f"Process at index {i} is invalid: {e}"}), 400

        if burst <= 0:
            return jsonify({"error": f"Process '{pid}' burst time must be > 0."}), 400
        if arrival < 0:
            return jsonify({"error": f"Process '{pid}' arrival time must be >= 0."}), 400

        normalised.append({"id": pid, "arrival": arrival, "burst": burst, "priority": prio})

    if algorithm == "RR":
        try:
            quantum = int(quantum)
            if quantum <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({"error": "Field 'quantum' must be a positive integer for Round Robin."}), 400

    # ── Dispatch ──────────────────────────────
    try:
        if algorithm == "FCFS":
            results, gantt, avg_tat, avg_wt = fcfs.run(normalised)

        elif algorithm == "SJF":
            results, gantt, avg_tat, avg_wt = sjf.run(normalised)

        elif algorithm == "SRTF":
            results, gantt, avg_tat, avg_wt = srtf.run(normalised)

        elif algorithm == "PRIORITY":
            results, gantt, avg_tat, avg_wt = priority.run_non_preemptive(normalised)

        elif algorithm == "PRIORITY_P":
            results, gantt, avg_tat, avg_wt = priority.run_preemptive(normalised)

        elif algorithm == "RR":
            results, gantt, avg_tat, avg_wt = round_robin.run(normalised, quantum)

    except Exception as e:
        return jsonify({"error": f"Simulation error: {str(e)}"}), 500

    # ── Save to DB ────────────────────────────
    try:
        db.save_result(algorithm, avg_tat, avg_wt)
    except Exception:
        pass  # Don't fail the response if DB write fails

    return jsonify({
        "algorithm": algorithm,
        "quantum": quantum if algorithm == "RR" else None,
        "results": results,
        "gantt": gantt,
        "avg_tat": avg_tat,
        "avg_wt": avg_wt,
    })


# ─────────────────────────────────────────────
# /history  GET
# ─────────────────────────────────────────────
@app.route("/history", methods=["GET"])
def history():
    rows = db.get_history()
    return jsonify(rows)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
    
