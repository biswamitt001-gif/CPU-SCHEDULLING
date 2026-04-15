"""
Priority Scheduling - Non-Preemptive and Preemptive variants.
Lower priority number = higher priority (1 is highest).
"""


def run_non_preemptive(processes):
    procs = [dict(p) for p in processes]
    n = len(procs)
    done = [False] * n
    completed = []
    gantt = []
    current_time = 0
    finished = 0

    while finished < n:
        available = [
            i for i in range(n)
            if not done[i] and procs[i]["arrival"] <= current_time
        ]

        if not available:
            next_arr = min(procs[i]["arrival"] for i in range(n) if not done[i])
            current_time = next_arr
            continue

        # Pick highest priority (lowest number), tie-break by arrival then id
        idx = min(available, key=lambda i: (procs[i]["priority"], procs[i]["arrival"], procs[i]["id"]))

        p = procs[idx]
        start = current_time
        end = start + p["burst"]

        gantt.append({"pid": p["id"], "start": start, "end": end})

        ct = end
        tat = ct - p["arrival"]
        wt = tat - p["burst"]

        completed.append({
            "id": p["id"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "ct": ct,
            "tat": tat,
            "wt": wt,
        })

        done[idx] = True
        current_time = end
        finished += 1

    avg_tat = sum(r["tat"] for r in completed) / len(completed)
    avg_wt = sum(r["wt"] for r in completed) / len(completed)

    return completed, gantt, round(avg_tat, 2), round(avg_wt, 2)


def run_preemptive(processes):
    """Preemptive Priority: at each time unit, run the highest-priority ready process."""
    procs = [dict(p) for p in processes]
    n = len(procs)
    remaining = [p["burst"] for p in procs]
    completion_time = [0] * n
    done = [False] * n

    gantt = []
    current_time = 0
    finished = 0
    prev_pid = None
    segment_start = 0

    while finished < n:
        available = [
            i for i in range(n)
            if not done[i] and procs[i]["arrival"] <= current_time
        ]

        if not available:
            if prev_pid is not None:
                gantt.append({"pid": prev_pid, "start": segment_start, "end": current_time})
                prev_pid = None
            current_time += 1
            continue

        idx = min(available, key=lambda i: (procs[i]["priority"], procs[i]["arrival"], procs[i]["id"]))
        current_pid = procs[idx]["id"]

        if current_pid != prev_pid:
            if prev_pid is not None:
                gantt.append({"pid": prev_pid, "start": segment_start, "end": current_time})
            segment_start = current_time
            prev_pid = current_pid

        remaining[idx] -= 1
        current_time += 1

        if remaining[idx] == 0:
            done[idx] = True
            finished += 1
            completion_time[idx] = current_time
            gantt.append({"pid": current_pid, "start": segment_start, "end": current_time})
            prev_pid = None

    # Merge consecutive same-pid segments
    merged = []
    for seg in gantt:
        if merged and merged[-1]["pid"] == seg["pid"] and merged[-1]["end"] == seg["start"]:
            merged[-1]["end"] = seg["end"]
        else:
            merged.append(dict(seg))

    results = []
    for i, p in enumerate(procs):
        ct = completion_time[i]
        tat = ct - p["arrival"]
        wt = tat - p["burst"]
        results.append({
            "id": p["id"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "ct": ct,
            "tat": tat,
            "wt": wt,
        })

    avg_tat = sum(r["tat"] for r in results) / len(results)
    avg_wt = sum(r["wt"] for r in results) / len(results)

    return results, merged, round(avg_tat, 2), round(avg_wt, 2)
