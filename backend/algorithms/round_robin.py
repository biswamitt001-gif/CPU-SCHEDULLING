"""
Round Robin Scheduling Algorithm (Preemptive) with configurable time quantum.
"""
from collections import deque


def run(processes, quantum):
    procs = [dict(p) for p in processes]
    n = len(procs)
    remaining = [p["burst"] for p in procs]
    completion_time = [0] * n

    # Sort by arrival for initial queue seeding
    order = sorted(range(n), key=lambda i: (procs[i]["arrival"], procs[i]["id"]))

    queue = deque()
    in_queue = [False] * n
    current_time = 0
    gantt = []

    def enqueue_arrived():
        """Ensure all processes that have arrived up to current_time are queued."""
        for i in order:
            if not in_queue[i] and procs[i]["arrival"] <= current_time:
                queue.append(i)
                in_queue[i] = True

    # Seed the first process at its actual arrival time
    first = order[0]
    current_time = procs[first]["arrival"]
    enqueue_arrived()

    while queue:
        idx = queue.popleft()
        p = procs[idx]

        exec_time = min(quantum, remaining[idx])
        start = current_time

        current_time += exec_time
        remaining[idx] -= exec_time

        # Enqueue any processes that arrived during this execution slice
        enqueue_arrived()

        end = current_time
        gantt.append({"pid": p["id"], "start": start, "end": end})

        # If process finishes or continues
        if remaining[idx] == 0:
            completion_time[idx] = current_time
        else:
            queue.append(idx)

        # Handle idle CPU: if queue is empty but processes remain
        if not queue:
            not_done = [j for j in range(n) if remaining[j] > 0 and not in_queue[j]]
            if not_done:
                next_j = min(not_done, key=lambda j: procs[j]["arrival"])
                current_time = max(current_time, procs[next_j]["arrival"])
                enqueue_arrived()

    # Merge consecutive same-pid gantt segments
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
