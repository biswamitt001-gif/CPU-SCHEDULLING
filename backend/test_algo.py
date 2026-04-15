import unittest
from algorithms import fcfs, sjf, srtf, priority, round_robin

class TestScheduling(unittest.TestCase):
    def test_fcfs(self):
        # Textbook FCFS edge: P1(0, 4), P2(1, 3)
        procs = [
            {"id": "P1", "arrival": 0, "burst": 4, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 1}
        ]
        res, gantt, t, w = fcfs.run(procs)
        self.assertEqual(t, 5.0) # P1(4)+P2(6) TAT = (4-0)+(7-1)=4+6=10. Avg = 5.0
        self.assertEqual(w, 1.5) # WT = 0 + 3 = 3. Avg = 1.5

    def test_sjf(self):
        # SJF Non-Preemptive
        # Arrives: P1(0, 6), P2(1, 4), P3(2, 2)
        # 0..6 P1, 6..8 P3, 8..12 P2
        procs = [
            {"id": "P1", "arrival": 0, "burst": 6, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 4, "priority": 1},
            {"id": "P3", "arrival": 2, "burst": 2, "priority": 1}
        ]
        res, gantt, t, w = sjf.run(procs)
        self.assertEqual(res[0]["id"], "P1") 
        self.assertEqual(res[1]["id"], "P3") 
        self.assertEqual(res[2]["id"], "P2")

    def test_srtf(self):
        # SRTF Preemptive
        # Arrives: P1(0, 8), P2(1, 4), P3(2, 2)
        # 0: P1 (rem 7 at 1). 1: P2(rem 4), so P2 preempts P1.
        # 2: P3(rem 2), P2(rem 3), P3 preempts P2.
        # P3 finishes at 4. P2 resumes and finishes at 7. P1 finishes at 14.
        procs = [
            {"id": "P1", "arrival": 0, "burst": 8, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 4, "priority": 1},
            {"id": "P3", "arrival": 2, "burst": 2, "priority": 1}
        ]
        res, gantt, t, w = srtf.run(procs)
        r = {p["id"]: p for p in res}
        self.assertEqual(r["P3"]["ct"], 4)
        self.assertEqual(r["P2"]["ct"], 7)
        self.assertEqual(r["P1"]["ct"], 14)

    def test_priority_np(self):
        # Priority NP (lower is better): P1(0, 5, p=2), P2(1, 3, p=1)
        # P1 starts at 0, finishes at 5. P2 starts at 5, finishes at 8.
        procs = [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 1}
        ]
        res, gantt, t, w = priority.run_non_preemptive(procs)
        self.assertEqual(res[0]["id"], "P1")
        self.assertEqual(res[1]["id"], "P2")
        
    def test_priority_p(self):
        # Priority Preemptive
        procs = [
            {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 1}
        ]
        res, gantt, t, w = priority.run_preemptive(procs)
        r = {p["id"]: p for p in res}
        self.assertEqual(r["P2"]["ct"], 4)
        self.assertEqual(r["P1"]["ct"], 8)

    def test_round_robin(self):
        # Round Robin Q=2
        # P1(0, 4), P2(1, 3)
        # 0..2 P1. Queue: P2, P1.
        # 2..4 P2. Queue: P1, P2.
        # 4..6 P1 (fin). Queue: P2.
        # 6..7 P2 (fin).
        procs = [
            {"id": "P1", "arrival": 0, "burst": 4, "priority": 1},
            {"id": "P2", "arrival": 1, "burst": 3, "priority": 1}
        ]
        res, gantt, t, w = round_robin.run(procs, 2)
        self.assertEqual(len(gantt), 4)
        self.assertEqual(gantt[0]["pid"], "P1")
        self.assertEqual(gantt[1]["pid"], "P2")
        self.assertEqual(gantt[2]["pid"], "P1")
        self.assertEqual(gantt[3]["pid"], "P2")

    def test_rr_idle_gap(self):
        # RR with an idle CPU gap
        procs = [
            {"id": "P1", "arrival": 0, "burst": 2, "priority": 1},
            {"id": "P2", "arrival": 5, "burst": 2, "priority": 1}
        ]
        res, gantt, t, w = round_robin.run(procs, 2)
        r = {p["id"]: p for p in res}
        self.assertEqual(r["P1"]["ct"], 2)
        self.assertEqual(r["P2"]["ct"], 7)

if __name__ == '__main__':
    unittest.main()
