# -*- coding: utf-8 -*-

"""
Compute the coarsest equitable partition (1-WL stable partition)
for all selected graph datasets in /content.

HumanPPI and WordNet are excluded.

For each graph G, the program stores:

    <graph>_equitable_vertex_colors.txt
    <graph>_cep_colors.npy

and creates a global summary:

    cep_summary.csv

The .npy file is useful for later comparison with the orbit partition.
"""

from collections import defaultdict
from array import array
from pathlib import Path
import numpy as np
import csv
import time
import gc
import sys


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path("/content")

OUTPUT_DIR = BASE_DIR / "cep_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# All datasets visible in your folder
ALL_DATASETS = [
    "Actors",
    "Amazon",
    "Astro-Ph",
    "CaliforniaRoads",
    "HumanDisease",
    "HumanPPI",
    "InternetAS-koblenz",
    "InternetAS-skitter",
    "LiveJournal",
    "OpenFlights",
    "USPowerGrid",
    "WordNet",
    "Yeast",
]


# Do not process these
EXCLUDED_DATASETS = {
    "HumanPPI",
    "WordNet",
}


# Same assumptions as in your previous code
HAS_HEADER = True

# Currently all graphs are treated as undirected.
#
# If later we discover that one of the .g files should actually
# be interpreted as directed, put its name here.
DIRECTED_DATASETS = set()


# Store a human-readable vertex -> cell file.
#
# For large graphs this file itself can become quite large,
# but it is useful for inspection.
SAVE_TEXT_VERTEX_COLORS = True


# ============================================================
# FILE READING
# ============================================================

def read_header_n(path):
    """
    Reads the first non-empty, non-comment line.

    Assumes that its first entry is the number of vertices.
    """

    with open(path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#") or line.startswith("%"):
                continue

            parts = line.split()

            return int(parts[0])

    raise ValueError("Could not read the header.")


def iter_edges(path, has_header=True):
    """
    Iterates over the edges of the graph.

    Example expected format:

        374511 15014839 1
        u v
        u v
        u v
        ...

    The first non-empty/non-comment line is skipped
    when has_header=True.
    """

    skipped_header = False

    with open(path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#") or line.startswith("%"):
                continue

            parts = line.split()

            if has_header and not skipped_header:
                skipped_header = True
                continue

            if len(parts) < 2:
                continue

            u = int(parts[0])
            v = int(parts[1])

            yield u, v


def detect_indexing_base(path, n, has_header=True):
    """
    Detect whether vertices are labelled

        0,...,n-1

    or

        1,...,n.

    Returns:
        0 for zero-based indexing
        1 for one-based indexing
    """

    min_id = None
    max_id = None

    for u, v in iter_edges(path, has_header=has_header):

        if min_id is None:
            min_id = min(u, v)
            max_id = max(u, v)

        else:
            min_id = min(min_id, u, v)
            max_id = max(max_id, u, v)

    if min_id is None:
        raise ValueError("No edges found in the graph.")

    if min_id == 0:
        return 0

    if max_id == n:
        return 1

    print(
        "Warning: could not determine indexing unambiguously. "
        "Assuming 0-based indexing.",
        file=sys.stderr,
    )

    return 0


def build_adjacency(path, has_header=True, directed=False):
    """
    Construct adjacency lists.

    Returns:

        adj
        output_base
        edge_count
    """

    path = Path(path)

    if has_header:

        n = read_header_n(path)

    else:

        max_id = -1
        min_id = None

        for u, v in iter_edges(path, has_header=False):

            max_id = max(max_id, u, v)

            min_id = (
                min(u, v)
                if min_id is None
                else min(min_id, u, v)
            )

        if min_id == 0:
            n = max_id + 1
        else:
            n = max_id


    print(f"Number of vertices from file: {n:,}")


    output_base = detect_indexing_base(
        path,
        n,
        has_header=has_header
    )


    if output_base == 0:
        print("Detected vertex labels: 0-based")
    else:
        print("Detected vertex labels: 1-based")


    # array("I") is much more memory efficient than Python lists
    # for large graphs.
    adj = [array("I") for _ in range(n)]


    edge_count = 0


    for u, v in iter_edges(path, has_header=has_header):

        u -= output_base
        v -= output_base


        if not (0 <= u < n):
            raise ValueError(
                f"Vertex {u + output_base} is out of range."
            )

        if not (0 <= v < n):
            raise ValueError(
                f"Vertex {v + output_base} is out of range."
            )


        if directed:

            adj[u].append(v)

        else:

            if u == v:
                adj[u].append(v)

            else:
                adj[u].append(v)
                adj[v].append(u)


        edge_count += 1


        if edge_count % 1_000_000 == 0:
            print(f"Read {edge_count:,} edges...")


    print("Finished reading graph.")
    print(f"Number of edges read from file: {edge_count:,}")


    return adj, output_base, edge_count


# ============================================================
# COARSEST EQUITABLE PARTITION
# ============================================================

def coarsest_equitable_partition(adj):
    """
    Computes the coarsest equitable partition obtained
    from the trivial partition.

    This is exactly the stable partition obtained by 1-WL
    when every vertex initially has the same color.

    Returns:

        color[v]      = cell ID of vertex v
        num_cells     = number of cells
        num_iterations
    """

    n = len(adj)


    # Start with the trivial partition:
    #
    #       {V}
    #
    color = array("I", [0]) * n

    num_colors = 1

    iteration = 0


    while True:

        iteration += 1

        signature_to_new_color = {}

        new_color = array("I", [0]) * n

        next_color = 0


        for v in range(n):

            neighbour_color_counts = {}


            for w in adj[v]:

                c = color[w]

                neighbour_color_counts[c] = (
                    neighbour_color_counts.get(c, 0) + 1
                )


            # Including color[v] guarantees refinement:
            #
            # cells may split, but different old cells
            # can never merge.
            signature = (
                color[v],
                tuple(
                    sorted(
                        neighbour_color_counts.items()
                    )
                )
            )


            if signature not in signature_to_new_color:

                signature_to_new_color[signature] = next_color
                next_color += 1


            new_color[v] = signature_to_new_color[signature]


        print(
            f"Iteration {iteration}: "
            f"{next_color:,} cells"
        )


        # Since this is a refinement process, the number of
        # cells can never decrease.
        #
        # If it did not increase, no cell was split, hence the
        # partition is stable.
        if next_color == num_colors:

            print("Stable partition reached.")

            return (
                new_color,
                next_color,
                iteration,
            )


        color = new_color
        num_colors = next_color


# ============================================================
# OUTPUT
# ============================================================

def write_vertex_colors(
    color,
    output_path,
    output_base=0
):
    """
    Writes

        vertex_id equitable_cell_id

    one vertex per line.
    """

    with open(output_path, "w") as f:

        f.write(
            "# vertex_id equitable_cell_id\n"
        )

        for v, c in enumerate(color):

            f.write(
                f"{v + output_base} {c}\n"
            )


def save_binary_colors(color, output_path):
    """
    Save cell assignments efficiently as a NumPy array.

    Entry i is the CEP cell of vertex i.

    This will be especially convenient for the later
    orbit-partition comparison.
    """

    colors_np = np.frombuffer(
        color,
        dtype=np.uint32
    )

    np.save(
        output_path,
        colors_np
    )


def write_summary(results, output_path):
    """
    Write/update the summary CSV.
    """

    fields = [
        "dataset",
        "status",
        "number_of_vertices",
        "number_of_edges",
        "number_of_cep_cells",
        "iterations",
        "indexing_base",
        "directed",
        "runtime_seconds",
    ]


    with open(
        output_path,
        "w",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields
        )

        writer.writeheader()

        for row in results:
            writer.writerow(row)


# ============================================================
# MAIN
# ============================================================

def main():

    datasets = [
        name
        for name in ALL_DATASETS
        if name not in EXCLUDED_DATASETS
    ]


    print("=" * 70)
    print("COARSEST EQUITABLE PARTITIONS")
    print("=" * 70)

    print()
    print("Datasets to process:")

    for name in datasets:
        print(f"  {name}")

    print()

    print("Excluded datasets:")

    for name in sorted(EXCLUDED_DATASETS):
        print(f"  {name}")

    print()


    summary_path = (
        OUTPUT_DIR /
        "cep_summary.csv"
    )

    results = []


    for i, graph_name in enumerate(
        datasets,
        start=1
    ):

        print()
        print("=" * 70)
        print(
            f"[{i}/{len(datasets)}] "
            f"{graph_name}"
        )
        print("=" * 70)


        graph_path = (
            BASE_DIR /
            f"{graph_name}.g"
        )


        if not graph_path.exists():

            print(
                f"WARNING: file not found: "
                f"{graph_path}"
            )

            results.append({
                "dataset": graph_name,
                "status": "FILE NOT FOUND",
                "number_of_vertices": "",
                "number_of_edges": "",
                "number_of_cep_cells": "",
                "iterations": "",
                "indexing_base": "",
                "directed": "",
                "runtime_seconds": "",
            })

            write_summary(
                results,
                summary_path
            )

            continue


        directed = (
            graph_name in DIRECTED_DATASETS
        )


        start_time = time.perf_counter()


        try:

            # ------------------------------------------------
            # 1. Read graph
            # ------------------------------------------------

            print()
            print("Step 1: Reading graph...")

            adj, output_base, edge_count = (
                build_adjacency(
                    graph_path,
                    has_header=HAS_HEADER,
                    directed=directed
                )
            )


            n = len(adj)


            # ------------------------------------------------
            # 2. CEP
            # ------------------------------------------------

            print()
            print(
                "Step 2: Computing coarsest "
                "equitable partition..."
            )

            (
                color,
                number_of_cells,
                iterations,
            ) = coarsest_equitable_partition(adj)


            # ------------------------------------------------
            # 3. Save
            # ------------------------------------------------

            print()
            print("Step 3: Saving partition...")


            binary_output = (
                OUTPUT_DIR /
                f"{graph_name}_cep_colors.npy"
            )


            save_binary_colors(
                color,
                binary_output
            )


            print(
                f"Saved binary partition:\n"
                f"    {binary_output}"
            )


            if SAVE_TEXT_VERTEX_COLORS:

                text_output = (
                    OUTPUT_DIR /
                    f"{graph_name}_equitable_vertex_colors.txt"
                )

                write_vertex_colors(
                    color,
                    text_output,
                    output_base=output_base
                )

                print(
                    f"Saved text partition:\n"
                    f"    {text_output}"
                )


            runtime = (
                time.perf_counter()
                - start_time
            )


            results.append({

                "dataset":
                    graph_name,

                "status":
                    "OK",

                "number_of_vertices":
                    n,

                "number_of_edges":
                    edge_count,

                "number_of_cep_cells":
                    number_of_cells,

                "iterations":
                    iterations,

                "indexing_base":
                    output_base,

                "directed":
                    directed,

                "runtime_seconds":
                    round(runtime, 3),
            })


            # Update after every graph.
            #
            # Thus, if Colab stops while processing a later
            # large graph, results for previous graphs are
            # already stored.
            write_summary(
                results,
                summary_path
            )


            print()
            print(
                f"Number of vertices: "
                f"{n:,}"
            )

            print(
                f"Number of edges: "
                f"{edge_count:,}"
            )

            print(
                f"Number of CEP cells: "
                f"{number_of_cells:,}"
            )

            print(
                f"Number of refinement iterations: "
                f"{iterations}"
            )

            print(
                f"Runtime: "
                f"{runtime:.2f} seconds"
            )


        except Exception as e:

            print()
            print(
                f"ERROR while processing "
                f"{graph_name}:"
            )

            print(e)


            results.append({

                "dataset":
                    graph_name,

                "status":
                    f"ERROR: {e}",

                "number_of_vertices":
                    "",

                "number_of_edges":
                    "",

                "number_of_cep_cells":
                    "",

                "iterations":
                    "",

                "indexing_base":
                    "",

                "directed":
                    directed,

                "runtime_seconds":
                    "",
            })


            write_summary(
                results,
                summary_path
            )


        finally:

            # Important for the large graphs.
            #
            # We do not want Actors / LiveJournal / Skitter
            # to remain in RAM while the next graph is loaded.

            if "adj" in locals():
                del adj

            if "color" in locals():
                del color

            gc.collect()


    print()
    print("=" * 70)
    print("ALL DATASETS FINISHED")
    print("=" * 70)

    print()
    print(
        "Summary stored at:"
    )

    print(summary_path)


if __name__ == "__main__":
    main()
