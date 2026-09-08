import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

OUTPUT_DIR = Path("/content/cep_outputs")

MAIN_RESULTS = OUTPUT_DIR / "cep_orbit_comparison.csv"
SPECIAL_RESULTS = OUTPUT_DIR / "HumanPPI_WordNet_comparison.csv"

FINAL_OUTPUT = OUTPUT_DIR / "all_13_cep_orbit_comparison.csv"


# ============================================================
# READ RESULTS
# ============================================================

df_main = pd.read_csv(MAIN_RESULTS)
df_special = pd.read_csv(SPECIAL_RESULTS)


# ============================================================
# KEEP THE COLUMNS WE NEED
# ============================================================

# First 11 datasets
df_main = df_main[
    [
        "dataset",
        "number_of_vertices",
        "number_of_cep_cells",
        "number_of_orbit_cells"
    ]
].copy()


# HumanPPI and WordNet
df_special = df_special[
    [
        "dataset",
        "number_of_vertices",
        "number_of_cep_cells",
        "number_of_orbit_cells"
    ]
].copy()


# ============================================================
# COMBINE ALL 13 DATASETS
# ============================================================

df = pd.concat(
    [df_main, df_special],
    ignore_index=True
)


# Sort alphabetically by dataset name
df = df.sort_values(
    "dataset"
).reset_index(drop=True)


# ============================================================
# COMPUTE COMPARISON AUTOMATICALLY
# ============================================================

df["Diff"] = (
    df["number_of_orbit_cells"]
    -
    df["number_of_cep_cells"]
)

df["Equal?"] = (
    df["number_of_cep_cells"]
    ==
    df["number_of_orbit_cells"]
)


# ============================================================
# RENAME COLUMNS FOR DISPLAY
# ============================================================

table = df.rename(
    columns={
        "dataset": "Dataset",
        "number_of_vertices": "n",
        "number_of_cep_cells": "CEP",
        "number_of_orbit_cells": "Orbits"
    }
)


# Keep only desired columns
table = table[
    [
        "Dataset",
        "n",
        "CEP",
        "Orbits",
        "Diff",
        "Equal?"
    ]
]


# ============================================================
# PRINT TABLE
# ============================================================

print("=" * 97)

print(
    f"{'Dataset':25s} "
    f"{'n':>12s} "
    f"{'CEP':>12s} "
    f"{'Orbits':>12s} "
    f"{'Diff':>10s} "
    f"{'Equal?':>8s}"
)

print("=" * 97)


for _, row in table.iterrows():

    print(
        f"{row['Dataset']:25s} "
        f"{int(row['n']):12,d} "
        f"{int(row['CEP']):12,d} "
        f"{int(row['Orbits']):12,d} "
        f"{int(row['Diff']):10,d} "
        f"{str(bool(row['Equal?'])):>8s}"
    )


print("=" * 97)


# ============================================================
# GLOBAL CONCLUSION
# ============================================================

print()

if table["Equal?"].all():

    print(
        "RESULT: CEP and orbit cell counts are equal "
        "for ALL datasets."
    )

else:

    print(
        "RESULT: CEP and orbit cell counts are NOT equal "
        "for all datasets."
    )

    print()
    print("Datasets where equality fails:")

    print(
        table.loc[
            ~table["Equal?"],
            [
                "Dataset",
                "CEP",
                "Orbits",
                "Diff"
            ]
        ].to_string(index=False)
    )


# ============================================================
# SAVE COMBINED RESULTS
# ============================================================

table.to_csv(
    FINAL_OUTPUT,
    index=False
)

print()
print("Combined table saved to:")
print(FINAL_OUTPUT)
