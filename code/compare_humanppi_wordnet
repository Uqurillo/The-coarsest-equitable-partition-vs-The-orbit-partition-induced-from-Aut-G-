# -*- coding: utf-8 -*-

"""
Compute the coarsest equitable partitions for

    HumanPPI
    WordNet

and align their labels with the corresponding .or files.

Procedure:

1. Compute CEP internally using 0-based Python indices.
2. Express the CEP using labels 1,...,n.
3. Apply the relabelling

       1 -> n
       i -> i-1   for i > 1

4. Compare the relabelled CEP with the automorphism orbit partition.

Each [...] block in a .or file is treated as one non-singleton orbit.
Vertices absent from the .or file are singleton orbits.
"""

from collections import defaultdict
from array import array
from pathlib import Path
import re
import csv
import gc
import time
import sys


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path("/content")

OUTPUT_DIR = BASE_DIR / "cep_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [
    "HumanPPI",
    "WordNet",
]

HAS_HEADER = True
DIRECTED = False


# ============================================================
# GRAPH READING
# ============================================================

def read_header_n(path):

    with open(path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#") or line.startswith("%"):
                continue

            return int(line.split()[0])

    raise ValueError("Could not read graph header.")


def iter_edges(path, has_header=True):

    skipped_header = False

    with open(path, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#") or line.startswith("%"):
                continue

            if has_header and not skipped_header:
                skipped_header = True
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            yield int(parts[0]), int(parts[1])


def detect_indexing_base(path, n, has_header=True):

    min_id = None
    max_id = None

    for u, v in iter_edges(path, has_header):

        if min_id is None:
            min_id = min(u, v)
            max_id = max(u, v)

        else:
            min_id = min(min_id, u, v)
            max_id = max(max_id, u, v)


    if min_id is None:
        raise ValueError("No edges found.")


    if min_id == 0:
        return 0

    if max_id == n:
        return 1


    print(
        "Could not determine indexing unambiguously; "
        "assuming 0-based.",
        file=sys.stderr,
    )

    return 0


def build_adjacency(path, has_header=True, directed=False):

    n = read_header_n(path)

    print(f"Number of vertices: {n:,}")


    input_base = detect_indexing_base(
        path,
        n,
        has_header
    )

    print(
        f".g file detected as "
        f"{input_base}-based"
    )


    adj = [
        array("I")
        for _ in range(n)
    ]


    edge_count = 0


    for u, v in iter_edges(path, has_header):

        u -= input_base
        v -= input_base


        if not (0 <= u < n):
            raise ValueError(f"Invalid vertex {u}")

        if not (0 <= v < n):
            raise ValueError(f"Invalid vertex {v}")


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
            print(
                f"Read {edge_count:,} edges..."
            )


    print(
        f"Finished reading "
        f"{edge_count:,} edges."
    )

    return adj, input_base, edge_count


# ============================================================
# COARSEST EQUITABLE PARTITION
# ============================================================

def coarsest_equitable_partition(adj):

    n = len(adj)

    color = array("I", [0]) * n

    number_of_colors = 1

    iteration = 0


    while True:

        iteration += 1

        signature_to_color = {}

        new_color = array("I", [0]) * n

        next_color = 0


        for v in range(n):

            counts = {}


            for w in adj[v]:

                c = color[w]

                counts[c] = (
                    counts.get(c, 0) + 1
                )


            signature = (
                color[v],
                tuple(sorted(counts.items()))
            )


            if signature not in signature_to_color:

                signature_to_color[
                    signature
                ] = next_color

                next_color += 1


            new_color[v] = (
                signature_to_color[signature]
            )


        print(
            f"Iteration {iteration}: "
            f"{next_color:,} cells"
        )


        if next_color == number_of_colors:

            print(
                "Stable partition reached."
            )

            return (
                new_color,
                next_color,
                iteration
            )


        color = new_color
        number_of_colors = next_color


# ============================================================
# CONVERT CEP TO CELLS
# ============================================================

def colors_to_cells_1_based(color):
    """
    CEP cells written using labels 1,...,n.

    Python vertex 0 -> label 1
    Python vertex 1 -> label 2
    ...
    Python vertex n-1 -> label n
    """

    cells = defaultdict(list)

    for v, c in enumerate(color):

        cells[int(c)].append(v + 1)


    result = list(cells.values())

    result.sort(
        key=lambda C: min(C)
    )

    return result


# ============================================================
# SPECIAL RELABELLING
# ============================================================

def rho(i, n):
    """
    Relabelling:

        1 -> n
        i -> i-1  for i > 1
    """

    if i == 1:
        return n

    return i - 1


def relabel_partition(cells, n):

    relabelled = []

    for cell in cells:

        new_cell = [
            rho(v, n)
            for v in cell
        ]

        new_cell.sort()

        relabelled.append(new_cell)


    relabelled.sort(
        key=lambda C: min(C)
    )

    return relabelled


# ============================================================
# READ .or FILE
# ============================================================

def read_orbit_partition(path, n):
    """
    Each [...] block is one non-singleton orbit.

    Vertices absent from the file are interpreted
    as singleton orbits.
    """

    non_singleton_orbits = []

    listed_vertices = set()


    with open(path, "r") as f:

        for line in f:

            blocks = re.findall(
                r"\[([^\]]*)\]",
                line
            )


            for block in blocks:

                orbit = [
                    int(x)
                    for x in re.findall(
                        r"\d+",
                        block
                    )
                ]


                if not orbit:
                    continue


                orbit.sort()

                non_singleton_orbits.append(
                    orbit
                )

                listed_vertices.update(
                    orbit
                )


    # .or files use labels 1,...,n here.
    singleton_vertices = (

        set(range(1, n + 1))
        -
        listed_vertices

    )


    partition = list(
        non_singleton_orbits
    )


    for v in singleton_vertices:
        partition.append([v])


    partition.sort(
        key=lambda C: (
            min(C),
            len(C),
            tuple(C)
        )
    )


    return partition


# ============================================================
# CANONICAL REPRESENTATION
# ============================================================

def canonical_partition(partition):
    """
    Converts a partition to a representation where
    ordering of cells and ordering inside cells do not matter.
    """

    return frozenset(
        frozenset(cell)
        for cell in partition
    )


# ============================================================
# WRITE CELLS
# ============================================================

def write_cells(cells, path):

    with open(path, "w") as f:

        for cell in cells:

            f.write("[")
            f.write(
                " ".join(map(str, cell))
            )
            f.write("]\n")


# ============================================================
# MAIN
# ============================================================

results = []


for dataset in DATASETS:

    print()
    print("=" * 75)
    print(dataset)
    print("=" * 75)


    graph_path = (
        BASE_DIR /
        f"{dataset}.g"
    )

    orbit_path = (
        BASE_DIR /
        f"{dataset}.or"
    )


    if not graph_path.exists():

        print(
            f"Graph file not found: "
            f"{graph_path}"
        )

        continue


    if not orbit_path.exists():

        print(
            f"Orbit file not found: "
            f"{orbit_path}"
        )

        continue


    start = time.perf_counter()


    # --------------------------------------------------------
    # 1. READ GRAPH
    # --------------------------------------------------------

    print()
    print("Step 1: Reading graph")

    adj, input_base, edge_count = (
        build_adjacency(
            graph_path,
            HAS_HEADER,
            DIRECTED
        )
    )

    n = len(adj)


    # --------------------------------------------------------
    # 2. COMPUTE CEP
    # --------------------------------------------------------

    print()
    print("Step 2: Computing CEP")

    (
        color,
        number_cep_cells,
        iterations
    ) = coarsest_equitable_partition(adj)


    # --------------------------------------------------------
    # 3. WRITE CEP USING 1-BASED LABELS
    # --------------------------------------------------------

    print()
    print(
        "Step 3: Converting CEP "
        "to 1-based labels"
    )

    cep_1_based = (
        colors_to_cells_1_based(color)
    )


    cep_1_based_path = (
        OUTPUT_DIR /
        f"{dataset}_cep_1based.txt"
    )


    write_cells(
        cep_1_based,
        cep_1_based_path
    )


    # --------------------------------------------------------
    # 4. APPLY rho
    # --------------------------------------------------------

    print()
    print(
        "Step 4: Applying relabelling rho"
    )

    cep_relabelled = (
        relabel_partition(
            cep_1_based,
            n
        )
    )


    relabelled_path = (
        OUTPUT_DIR /
        f"{dataset}_cep_relabelled.txt"
    )


    write_cells(
        cep_relabelled,
        relabelled_path
    )


    # --------------------------------------------------------
    # 5. READ ORBIT PARTITION
    # --------------------------------------------------------

    print()
    print(
        "Step 5: Reading orbit partition"
    )

    orbit_partition = (
        read_orbit_partition(
            orbit_path,
            n
        )
    )


    number_orbit_cells = len(
        orbit_partition
    )


    # --------------------------------------------------------
    # 6. COMPARE
    # --------------------------------------------------------

    equal_counts = (
        number_cep_cells
        ==
        number_orbit_cells
    )


    equal_partitions = (

        canonical_partition(
            cep_relabelled
        )

        ==

        canonical_partition(
            orbit_partition
        )
    )


    runtime = (
        time.perf_counter() - start
    )


    print()
    print("-" * 75)

    print(
        f"Number of vertices: "
        f"{n:,}"
    )

    print(
        f"Number of CEP cells: "
        f"{number_cep_cells:,}"
    )

    print(
        f"Number of orbit cells: "
        f"{number_orbit_cells:,}"
    )

    print(
        f"Cell counts equal: "
        f"{equal_counts}"
    )

    print(
        "Relabelled CEP equals "
        f"orbit partition: "
        f"{equal_partitions}"
    )

    print(
        f"Runtime: "
        f"{runtime:.2f} seconds"
    )

    print("-" * 75)


    results.append({

        "dataset":
            dataset,

        "number_of_vertices":
            n,

        "number_of_edges":
            edge_count,

        "number_of_cep_cells":
            number_cep_cells,

        "number_of_orbit_cells":
            number_orbit_cells,

        "counts_equal":
            equal_counts,

        "relabelled_partitions_equal":
            equal_partitions,

        "iterations":
            iterations,

        "runtime_seconds":
            round(runtime, 3),
    })


    # Free RAM
    del adj
    del color

    gc.collect()


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_path = (
    OUTPUT_DIR /
    "HumanPPI_WordNet_comparison.csv"
)


with open(
    summary_path,
    "w",
    newline=""
) as f:

    fieldnames = [

        "dataset",
        "number_of_vertices",
        "number_of_edges",
        "number_of_cep_cells",
        "number_of_orbit_cells",
        "counts_equal",
        "relabelled_partitions_equal",
        "iterations",
        "runtime_seconds",
    ]


    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)


print()
print("=" * 75)
print("FINISHED")
print("=" * 75)

print(
    f"Summary saved to:\n"
    f"{summary_path}"
)
