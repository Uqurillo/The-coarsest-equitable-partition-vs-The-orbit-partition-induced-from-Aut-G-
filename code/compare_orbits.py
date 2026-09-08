import re
import csv
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path("/content")

CEP_SUMMARY_PATH = (
    BASE_DIR
    / "cep_outputs"
    / "cep_summary.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "cep_outputs"
    / "cep_orbit_comparison.csv"
)


# ============================================================
# DATASETS
# ============================================================

DATASETS = [
    "Actors",
    "Amazon",
    "Astro-Ph",
    "CaliforniaRoads",
    "HumanDisease",
    "InternetAS-koblenz",
    "InternetAS-skitter",
    "LiveJournal",
    "OpenFlights",
    "USPowerGrid",
    "Yeast",
]


# ============================================================
# READ CEP SUMMARY
# ============================================================

def read_cep_summary(path):

    results = {}

    with open(path, "r", newline="") as f:

        reader = csv.DictReader(f)

        for row in reader:

            if row["status"] != "OK":
                continue

            results[row["dataset"]] = {
                "n": int(row["number_of_vertices"]),
                "cep_cells": int(row["number_of_cep_cells"]),
            }

    return results


# ============================================================
# READ .or FILE
# ============================================================

def read_orbit_information(path, n):
    """
    Each bracketed block in the .or file represents
    ONE non-singleton orbit.

    Examples:

        [956 1634]

    represents one orbit.

        [598 776] * [676 1201]

    represents TWO distinct orbits.

    Vertices not occurring anywhere in the .or file
    are interpreted as singleton orbits.
    """

    non_singleton_orbits = []

    listed_vertices = set()

    duplicate_vertices = set()

    invalid_vertices = []


    with open(path, "r") as f:

        for line_number, line in enumerate(f, start=1):

            # Extract every separate [...]
            # expression on the line.
            blocks = re.findall(
                r"\[([^\]]*)\]",
                line
            )

            for block in blocks:

                vertices = [
                    int(x)
                    for x in re.findall(r"\d+", block)
                ]

                if not vertices:
                    continue

                # Every bracket is one orbit
                non_singleton_orbits.append(vertices)


                for v in vertices:

                    # .or files are 0-based
                    if not (0 <= v < n):

                        invalid_vertices.append(
                            (line_number, v)
                        )

                    if v in listed_vertices:
                        duplicate_vertices.add(v)

                    listed_vertices.add(v)


    number_non_singleton = len(
        non_singleton_orbits
    )

    number_listed_vertices = len(
        listed_vertices
    )

    number_singletons = (
        n - number_listed_vertices
    )

    number_orbit_cells = (
        number_non_singleton
        + number_singletons
    )


    return {

        "number_non_singleton_orbits":
            number_non_singleton,

        "number_listed_vertices":
            number_listed_vertices,

        "number_singleton_orbits":
            number_singletons,

        "number_orbit_cells":
            number_orbit_cells,

        "duplicate_vertices":
            duplicate_vertices,

        "invalid_vertices":
            invalid_vertices,
    }


# ============================================================
# MAIN COMPARISON
# ============================================================

cep_summary = read_cep_summary(
    CEP_SUMMARY_PATH
)

results = []


print("=" * 95)

print(
    f"{'Dataset':25s} "
    f"{'n':>10s} "
    f"{'CEP':>12s} "
    f"{'Orbits':>12s} "
    f"{'Diff':>10s} "
    f"{'Equal?':>8s}"
)

print("=" * 95)


for dataset in DATASETS:

    if dataset not in cep_summary:

        print(
            f"{dataset:25s} "
            "CEP result not found."
        )

        continue


    n = cep_summary[dataset]["n"]

    cep_cells = (
        cep_summary[dataset]["cep_cells"]
    )


    orbit_path = (
        BASE_DIR /
        f"{dataset}.or"
    )


    if not orbit_path.exists():

        print(
            f"{dataset:25s} "
            f"Orbit file not found: {orbit_path}"
        )

        continue


    orbit_info = read_orbit_information(
        orbit_path,
        n
    )


    orbit_cells = (
        orbit_info["number_orbit_cells"]
    )

    difference = (
        orbit_cells - cep_cells
    )

    equal = (
        orbit_cells == cep_cells
    )


    # ----------------------------------------
    # Sanity checks
    # ----------------------------------------

    if orbit_info["invalid_vertices"]:

        status = "INVALID VERTEX IDS"

    elif orbit_info["duplicate_vertices"]:

        status = "DUPLICATE VERTICES"

    elif difference < 0:

        # This should not happen because
        #
        # pi_orbit refines pi_CEP.
        status = "ERROR: ORBITS < CEP"

    elif equal:

        status = "EQUAL"

    else:

        status = "STRICTLY FINER"


    print(
        f"{dataset:25s} "
        f"{n:10,d} "
        f"{cep_cells:12,d} "
        f"{orbit_cells:12,d} "
        f"{difference:10,d} "
        f"{str(equal):>8s}"
    )


    results.append({

        "dataset":
            dataset,

        "number_of_vertices":
            n,

        "number_of_cep_cells":
            cep_cells,

        "number_of_non_singleton_orbits":
            orbit_info[
                "number_non_singleton_orbits"
            ],

        "number_of_vertices_in_non_singleton_orbits":
            orbit_info[
                "number_listed_vertices"
            ],

        "number_of_singleton_orbits":
            orbit_info[
                "number_singleton_orbits"
            ],

        "number_of_orbit_cells":
            orbit_cells,

        "orbit_minus_cep":
            difference,

        "partitions_equal":
            equal,

        "status":
            status,
    })


# ============================================================
# SAVE RESULTS
# ============================================================

fieldnames = [

    "dataset",

    "number_of_vertices",

    "number_of_cep_cells",

    "number_of_non_singleton_orbits",

    "number_of_vertices_in_non_singleton_orbits",

    "number_of_singleton_orbits",

    "number_of_orbit_cells",

    "orbit_minus_cep",

    "partitions_equal",

    "status",
]


with open(
    OUTPUT_PATH,
    "w",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(results)


print("=" * 95)

print()
print("Comparison saved to:")
print(OUTPUT_PATH)
