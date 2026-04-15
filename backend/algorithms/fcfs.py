"""
First Come First Serve (FCFS) Scheduling Algorithm
Non-preemptive: processes are executed in arrival order.
"""


def run(processes):
    """
    processes: list of dicts with keys: id, arrival, burst, priority
    Returns: (results, gantt)
        results: list of dicts with id, arrival, burst, ct, tat, wt
        gantt:   list of dicts with pid, start, end
    """
    # Sort by arrival time (tie-break by original order / id)
    procs = sorted(processes, key=lambda p: (p["arrival"], p["id"]))

    gantt = []
    results = []
    current_time = 0

    for p in procs:
        start = max(current_time, p["arrival"])
        end = start + p["burst"]

        gantt.append({"pid": p["id"], "start": start, "end": end})

        ct = end
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

        current_time = end

    avg_tat = sum(r["tat"] for r in results) / len(results)
    avg_wt = sum(r["wt"] for r in results) / len(results)

    return results, gantt, round(avg_tat, 2), round(avg_wt, 2)
