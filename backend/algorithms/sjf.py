"""
Shortest Job First (SJF) - Non-Preemptive
At each selection point, pick the ready process with the smallest burst time.
"""


def run(processes):
    procs = [dict(p) for p in processes]  # copy
    n = len(procs)
    completed = []
    gantt = []
    done = [False] * n
    current_time = 0
    finished = 0

    while finished < n:
        # Find all processes that have arrived and are not done
        available = [
            i for i in range(n)
            if not done[i] and procs[i]["arrival"] <= current_time
        ]

        if not available:
            # CPU idle — jump to next arrival
            next_arrival = min(procs[i]["arrival"] for i in range(n) if not done[i])
            current_time = next_arrival
            continue

        # Pick shortest burst (tie-break: earliest arrival, then id)
        idx = min(available, key=lambda i: (procs[i]["burst"], procs[i]["arrival"], procs[i]["id"]))

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
