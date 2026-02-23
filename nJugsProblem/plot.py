import json
import matplotlib.pyplot as plt

from the3jugs import NJugsProblem
from solvers import BFSSearch, DFSSearch

def load_cases(path="test_cases.json"):
    with open(path, "r") as f:
        return json.load(f)

def main():
    cases = load_cases("test_cases.json")

    bfs_rows = []
    dfs_rows = []

    for case in cases:
        caps = case["capacities"]
        goal = case["goal"]
        s = sum(int(c) for c in caps)

        problem = NJugsProblem(caps, goal)

        bfs = BFSSearch(problem).solve()
        dfs = DFSSearch(problem).solve()

        bfs_rows.append((s, bfs["b"], bfs["d"], bfs["time"]))
        dfs_rows.append((s, dfs["b"], dfs["D"], dfs["time"]))

    # Sort by sum of capacities
    bfs_rows.sort(key=lambda x: x[0])
    dfs_rows.sort(key=lambda x: x[0])

    # --- Plot BFS: b and d on left axis, time on right ---
    xs = [r[0] for r in bfs_rows]
    bvals = [r[1] for r in bfs_rows]
    dvals = [r[2] if r[2] is not None else float("nan") for r in bfs_rows]
    tvals = [r[3] for r in bfs_rows]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(xs, bvals, marker="o", label="Branching factor b")
    ax1.plot(xs, dvals, marker="s", label="Shallowest solution depth d")
    ax2.plot(xs, tvals, marker="^", label="Time (s)")

    ax1.set_xlabel("Sum of capacities")
    ax1.set_ylabel("b and d")
    ax2.set_ylabel("Execution time (s)")
    ax1.set_title("BFS scaling: branching factor, depth, and time")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

    plt.tight_layout()
    plt.show()

    # --- Plot DFS: b and D on left axis, time on right ---
    xs = [r[0] for r in dfs_rows]
    bvals = [r[1] for r in dfs_rows]
    Dvals = [r[2] for r in dfs_rows]
    tvals = [r[3] for r in dfs_rows]

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(xs, bvals, marker="o", label="Branching factor b")
    ax1.plot(xs, Dvals, marker="s", label="Max depth reached D")
    ax2.plot(xs, tvals, marker="^", label="Time (s)")

    ax1.set_xlabel("Sum of capacities")
    ax1.set_ylabel("b and D")
    ax2.set_ylabel("Execution time (s)")
    ax1.set_title("DFS scaling: branching factor, depth, and time")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
