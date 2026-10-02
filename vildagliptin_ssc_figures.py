# -*- coding: utf-8 -*-
"""Vildagliptin for systemic sclerosis: hackathon figure notebook.

Exported from a Google Colab notebook. Runs only in Colab: it mounts Google
Drive, loads pre-computed results from ``colab_upload.zip`` (not included in
this repository) and renders the presentation figures. No statistics are
recomputed here; see README.md.

# Vildagliptin repurposing for systemic sclerosis

### DPP-4/CD26 → progenitor/ECM-associated fibroblast state → cutaneous fibrosis

---

## Hypothesis

We propose repurposing **vildagliptin** for **cutaneous fibrosis in systemic sclerosis (SSc)** because the drug inhibits **DPP-4/CD26**, a target functionally linked to fibroblast biology and fibrosis.

Our hypothesis does **not** require global DPP4 upregulation in SSc skin. Instead, we test whether DPP4 identifies a **disease-relevant progenitor/ECM-associated fibroblast state** that can be pharmacologically modulated.

---

## Central question

**Does the biology of DPP-4/CD26 in human SSc fibroblasts, together with the pharmacology of vildagliptin, justify advancing the drug to disease-relevant proof-of-mechanism testing?**

---

## Validation strategy

**Human disease context** → **Cellular localization and state** → **Clinical relevance** → **Mechanistic organization** → **Drug translation** → **Stress tests and limitations**

- **Human disease context:** fibrotic / ECM-remodeling program in SSc skin  
- **Cellular localization and state:** DPP4 distribution across skin cell types and fibroblast states  
- **Clinical relevance:** association between fibroblast programs and mRSS  
- **Mechanistic organization:** trajectory, regulatory activity, and network medicine  
- **Drug translation:** functional evidence plus human pharmacology of vildagliptin  
- **Stress tests and limitations:** perturbational transcriptomics, human genetics, and contrary evidence  

---

## Model being tested

**Vildagliptin** → **DPP-4 / CD26 inhibition** → **DPP4-associated progenitor / ECM fibroblast context** → **fibroblast activation and matrix-remodeling programs** → **cutaneous fibrosis in SSc**

> This model represents a disease-relevant functional association, **not a mandatory linear fibroblast trajectory**.

---

## Objective

Determine whether the convergence of **human disease evidence, fibroblast-state biology, functional mechanism, and pharmacology** is sufficient to justify a **disease-relevant dermal proof-of-mechanism experiment** — **not a claim of clinical efficacy**.
"""

# @title 1. Initialize session and load DaVinci results {display-mode: "form"}
# @markdown Prepare the visualization environment and load the curated `colab_upload.zip` directly from Google Drive.
# @markdown
# @markdown All scientific analyses were previously executed on **DaVinci through Slurm**.
# @markdown Imported results are verified against their **SHA256 hashes** before use.

import sys
import os
import subprocess
import importlib.metadata as metadata


# ============================================================
# 1. NOTEBOOK DEPENDENCIES
# ============================================================
#
# Install BEFORE importing Plotly anywhere in the notebook.
# Plotly 6.1.1+ is required for Kaleido v1 static export.
# ============================================================

subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "--upgrade",
        "plotly>=6.1.1,<7",
        "kaleido>=1.0.0,<2",
        "graphviz",
        "pyvis",
        "ete3",
    ],
    check=True,
)


def version_tuple(version):
    """Convert a version string to a ``(major, minor)`` tuple.

    Parameters
    ----------
    version : str
        Version string such as ``"6.1.1"``.

    Returns
    -------
    tuple of int
        The first two numeric components, e.g. ``(6, 1)``.
    """
    return tuple(
        int(x)
        for x in version.split(".")[:2]
    )


installed_plotly = metadata.version("plotly")
installed_kaleido = metadata.version("kaleido")


# ============================================================
# 2. STALE-MODULE PROTECTION
# ============================================================
#
# If an old Plotly version was already imported before this cell,
# restart the Python kernel automatically.
#
# pip-installed packages remain available after the restart.
# Run this same cell again after the automatic restart.
# ============================================================

loaded_plotly_module = sys.modules.get("plotly")

if loaded_plotly_module is not None:

    loaded_plotly_version = getattr(
        loaded_plotly_module,
        "__version__",
        "0.0.0",
    )

    if version_tuple(loaded_plotly_version) < (6, 1):

        print("=" * 64)
        print("VISUALIZATION ENVIRONMENT UPDATE")
        print("=" * 64)
        print(f"Plotly loaded    : {loaded_plotly_version}")
        print(f"Plotly installed : {installed_plotly}")
        print()
        print("A previous Plotly version is still loaded in memory.")
        print("Restarting the Python kernel automatically...")
        print()
        print("After the restart, run Cell 1 again.")

        # Flush text before restarting.
        sys.stdout.flush()

        os.kill(
            os.getpid(),
            9
        )


# ============================================================
# 3. DATA IMPORTS
# ============================================================

from google.colab import drive
from pathlib import Path

import zipfile
import hashlib
import shutil
import pandas as pd


# ============================================================
# 4. WORKSPACE
# ============================================================

WORKDIR = Path(
    "/content/vildagliptin_ssc"
)

DATA = WORKDIR / "data"


# Start from a clean workspace (Colab /content path).
if WORKDIR.exists():
    shutil.rmtree(
        WORKDIR
    )


DATA.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 5. LOAD CURATED EVIDENCE BUNDLE FROM GOOGLE DRIVE
# ============================================================

drive.mount(
    "/content/drive"
)


DRIVE_ROOT = Path(
    "/content/drive/MyDrive"
)


print()
print("Searching Google Drive for colab_upload.zip...")


zip_hits = list(
    DRIVE_ROOT.rglob(
        "colab_upload.zip"
    )
)


if len(zip_hits) == 0:

    # Diagnostic information: show ZIP files that do exist.
    available_zips = list(
        DRIVE_ROOT.rglob(
            "*.zip"
        )
    )

    print()
    print("Could not find 'colab_upload.zip'.")

    if available_zips:

        print()
        print("ZIP files found in MyDrive:")

        for path in available_zips:
            print(
                f"  - {path}"
            )

    else:

        print()
        print(
            "No ZIP files were found anywhere in MyDrive."
        )

    raise FileNotFoundError(
        "Could not find 'colab_upload.zip' anywhere "
        "inside Google Drive/MyDrive."
    )


if len(zip_hits) > 1:

    print()
    print(
        "Multiple copies of colab_upload.zip were found:"
    )

    for path in zip_hits:
        print(
            f"  - {path}"
        )

    raise RuntimeError(
        "Multiple copies of 'colab_upload.zip' were found. "
        "Please keep only one copy or specify its path explicitly."
    )


zip_path = zip_hits[0]


print()
print(
    f"Using curated evidence bundle: {zip_path}"
)


# ============================================================
# 6. EXTRACT
# ============================================================

with zipfile.ZipFile(
    zip_path,
    "r"
) as archive:

    archive.extractall(
        DATA
    )


# ============================================================
# 7. LOCATE CURATED MANIFEST
# ============================================================

inventory_hits = list(
    DATA.rglob(
        "colab_inventory.tsv"
    )
)


if len(inventory_hits) != 1:

    raise RuntimeError(
        "Could not uniquely locate "
        "colab_inventory.tsv."
    )


INVENTORY_PATH = inventory_hits[0]

# All curated notebook files live in this same directory.
DATA = INVENTORY_PATH.parent


inventory = pd.read_csv(
    INVENTORY_PATH,
    sep="\t"
)


# ============================================================
# 8. SHA256 INTEGRITY CHECK
# ============================================================

def sha256_file(path):
    """Compute the SHA256 hex digest of a file.

    Parameters
    ----------
    path : pathlib.Path
        File to hash; read in 1 MiB blocks.

    Returns
    -------
    str
        Lower-case hexadecimal SHA256 digest.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:

        for block in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(
                block
            )

    return digest.hexdigest()


checks = []


for _, row in inventory.iterrows():

    path = (
        DATA
        /
        row["File"]
    )

    exists = path.exists()

    observed_sha = (
        sha256_file(path)
        if exists
        else None
    )

    expected_sha = str(
        row["SHA256"]
    ).lower()


    checks.append({
        "file":
            row["File"],

        "exists":
            exists,

        "sha256_match":
            (
                observed_sha
                ==
                expected_sha
            )
            if exists
            else False,
    })


integrity = pd.DataFrame(
    checks
)


n_expected = len(
    integrity
)

n_present = int(
    integrity[
        "exists"
    ].sum()
)

n_valid = int(
    integrity[
        "sha256_match"
    ].sum()
)


# ============================================================
# 9. FINAL STATUS
# ============================================================

print()
print("=" * 64)
print("REPRODUCIBLE DATA IMPORT")
print("=" * 64)

print(
    f"ZIP source          : {zip_path}"
)

print(
    f"Dataset directory   : {DATA}"
)

print(
    f"Expected files      : {n_expected}"
)

print(
    f"Files found         : {n_present}"
)

print(
    f"Valid SHA256 hashes : {n_valid}"
)

print(
    f"Plotly installed    : {installed_plotly}"
)

print(
    f"Kaleido installed   : {installed_kaleido}"
)


if (
    n_present == n_expected
    and
    n_valid == n_expected
):

    print()
    print(
        "✓ DATASET INTEGRITY: PASS"
    )

else:

    print()
    print(
        "✗ DATASET INTEGRITY: FAIL"
    )

    # `display` is an IPython built-in in Colab; it is not imported here.
    display(
        integrity[
            (~integrity["exists"])
            |
            (~integrity["sha256_match"])
        ]
    )

    raise RuntimeError(
        "Dataset integrity validation failed."
    )


# ============================================================
# 10. GLOBAL NOTEBOOK PATH
# ============================================================

COLAB_DATA = DATA

# @title 2. Initialize visualization environment {display-mode: "form"}
# @markdown Prepare the libraries used to **visualize** the processed DaVinci results.
# @markdown
# @markdown Scientific analyses were already performed on **DaVinci through Slurm**.
# @markdown This cell only prepares the notebook for interactive visualization and figure generation.

# NOTE: IPython shell magic. Valid only in Colab/Jupyter; it makes this
# exported .py file unparseable as plain Python. Repeats the install in cell 1.
!pip -q install --upgrade \
    "plotly>=6.1.1" \
    "kaleido>=1.0.0" \
    graphviz \
    pyvis \
    ete3

from pathlib import Path
from IPython.display import display, HTML, Image, SVG

import re
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly
import plotly.express as px
import plotly.graph_objects as go

# networkx, graphviz and pyvis are imported but not used by any cell below.
import networkx as nx

from graphviz import Digraph
from pyvis.network import Network

# ============================================================
# STATIC FIGURE EXPORT SUPPORT
# ============================================================

import kaleido

try:
    kaleido.get_chrome_sync()
except Exception:
    pass
# ============================================================
# VALIDATED DATA DIRECTORY
# ============================================================

if "COLAB_DATA" not in globals():
    raise RuntimeError(
        "COLAB_DATA is not defined. Run Cell 1 first."
    )

DATA = Path(COLAB_DATA)

if not DATA.exists():
    raise RuntimeError(
        f"Validated data directory not found: {DATA}"
    )


# ============================================================
# DATA ACCESS HELPERS
# ============================================================

def data_file(name):
    """Return the path of a file in the validated data directory.

    Parameters
    ----------
    name : str
        File name relative to ``DATA``.

    Returns
    -------
    pathlib.Path
        Full path to the file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    path = DATA / name

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {name}"
        )

    return path


def load_tsv(name):
    """Load a tab-separated result table from the data directory.

    Parameters
    ----------
    name : str
        TSV file name relative to ``DATA``.

    Returns
    -------
    pandas.DataFrame
        The loaded table.
    """
    return pd.read_csv(
        data_file(name),
        sep="\t"
    )


def show_png(name, width=900):
    """Display a PNG from the data directory in the notebook.

    Parameters
    ----------
    name : str
        PNG file name relative to ``DATA``.
    width : int, default 900
        Display width in pixels.
    """
    display(
        Image(
            filename=str(data_file(name)),
            width=width
        )
    )


# ============================================================
# RESULT CATALOG
# ============================================================

files_available = sorted(
    p for p in DATA.iterdir()
    if p.is_file()
)


def analysis_id(filename):
    """Extract the analysis identifier from a result file name.

    Parameters
    ----------
    filename : str
        File name such as ``"R4b_Reactome_GSEA_delta.tsv"``.

    Returns
    -------
    str
        The ``R<number>[letter]`` prefix (e.g. ``"R4b"``), or ``"metadata"``
        if the name has no such prefix.
    """

    match = re.match(
        r"^(R\d+[a-z]?)_",
        filename
    )

    return (
        match.group(1)
        if match
        else "metadata"
    )


catalog = pd.DataFrame([
    {
        "file": p.name,
        "analysis": analysis_id(p.name),
        "type": p.suffix.lower().lstrip("."),
        "size_kb": round(
            p.stat().st_size / 1024,
            1
        ),
    }
    for p in files_available
])


print("=" * 64)
print("VISUALIZATION ENVIRONMENT")
print("=" * 64)

print(f"Validated data directory : {DATA}")
print(f"Available files          : {len(files_available)}")
print(f"Python                   : {sys.version.split()[0]}")
print(f"Pandas                   : {pd.__version__}")
print(f"Plotly                   : {plotly.__version__}")

print()
print("✓ VISUALIZATION ENVIRONMENT: READY")

# @title 3. Evidence architecture of the study {display-mode: "form"}
# @markdown Visual overview of the independent evidence layers used to test the repurposing hypothesis.
# @markdown
# @markdown Link widths represent **evidence layers only** and should not be interpreted as quantitative evidence strength.

import plotly.graph_objects as go


# ============================================================
# NODES
# ============================================================

labels = [
    "<b>Repurposing hypothesis</b><br>"
    "Vildagliptin → DPP4/CD26 → cutaneous SSc",

    "<b>Human disease biology</b><br>R1 · R3 · R4b",

    "<b>Cellular localization</b><br>R2 · R11",

    "<b>Fibroblast organization</b><br>R9 · R12",

    "<b>Network medicine</b><br>R4a · R10",

    "<b>Drug & pharmacology</b><br>R5 · R8",

    "<b>Translational gap</b><br>R6",

    "<b>Stress tests</b><br>R16 · R17",

    "<b>Integrated decision</b><br>"
    "Advance to proof-of-mechanism?"
]


# ============================================================
# TOOL / METHOD DETAILS FOR HOVER
# ============================================================

customdata = [
    (
        "Drug: vildagliptin<br>"
        "Target: DPP4/CD26<br>"
        "Disease: systemic sclerosis"
    ),

    (
        "Human bulk transcriptomics<br>"
        "Clinical mRSS association<br>"
        "Reactome pathway enrichment"
    ),

    (
        "Human skin single-cell RNA-seq<br>"
        "Scanpy / AnnData<br>"
        "Independent cohort replication"
    ),

    (
        "PAGA / pseudotime<br>"
        "PROGENy / CollecTRI<br>"
        "Fibroblast regulatory states"
    ),

    (
        "STRING v12<br>"
        "Degree-matched permutation null<br>"
        "Network proximity"
    ),

    (
        "Experimental literature<br>"
        "Human PK/PD<br>"
        "Dermal exposure sensitivity model"
    ),

    (
        "PubMed<br>"
        "Cortellis<br>"
        "ClinicalTrials.gov"
    ),

    (
        "LINCS perturbational signatures<br>"
        "GWAS Catalog<br>"
        "GTEx / Open Targets"
    ),

    (
        "Cross-layer synthesis<br>"
        "Supporting + contrary evidence<br>"
        "Go / no-go translational decision"
    ),
]


# ============================================================
# LINKS
# ============================================================

source = [
    0, 0, 0, 0, 0, 0, 0,
    1, 2, 3, 4, 5, 6, 7
]

target = [
    1, 2, 3, 4, 5, 6, 7,
    8, 8, 8, 8, 8, 8, 8
]

value = [1] * len(source)


# ============================================================
# FIXED LAYOUT
# ============================================================

x = [
    0.01,

    0.29,
    0.29,
    0.29,
    0.29,
    0.29,
    0.29,
    0.29,

    0.92
]

y = [
    0.48,

    0.04,
    0.19,
    0.34,
    0.49,
    0.64,
    0.79,
    0.94,

    0.48
]


# ============================================================
# FIGURE
# ============================================================

fig = go.Figure(
    go.Sankey(
        arrangement="fixed",

        node=dict(
            label=labels,
            customdata=customdata,
            x=x,
            y=y,
            pad=18,
            thickness=21,

            line=dict(
                width=0.7
            ),

            hovertemplate=(
                "%{label}<br><br>"
                "%{customdata}"
                "<extra></extra>"
            ),
        ),

        link=dict(
            source=source,
            target=target,
            value=value,

            hovertemplate=(
                "Independent evidence layer"
                "<extra></extra>"
            ),
        ),
    )
)


fig.update_layout(
    title=dict(
        text=(
            "<b>Evidence architecture of the repurposing study</b>"
            "<br>"
            "<sup>"
            "Independent human, mechanistic, pharmacological "
            "and contrary-evidence layers"
            "</sup>"
        ),

        x=0.5,
        xanchor="center"
    ),

    font=dict(
        size=13
    ),

    height=650,

    margin=dict(
        l=20,
        r=20,
        t=85,
        b=25
    )
)


fig.show()

# @title 4. Human SSc skin shows a strong fibrotic/ECM program {display-mode: "form"}
# @markdown **Question:** Is the biological process targeted by the repurposing hypothesis present in human systemic sclerosis skin?
# @markdown
# @markdown **Data:** GSE58095 human skin transcriptomics
# @markdown **Analysis:** SSc vs control differential expression + Reactome GSEA
# @markdown **Analysis tools:** Python · scipy/statsmodels · Reactome/GSEA
# @markdown **Visualization:** Plotly

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from IPython.display import display, HTML

# ============================================================
# LOAD DATA
# ============================================================

genes = load_tsv("R1_target_gene_case_control.tsv")
reactome = load_tsv("R4b_Reactome_GSEA_delta.tsv")

# ============================================================
# PANEL A — PRE-SPECIFIED FIBROTIC GENES
# ============================================================

genes_of_interest = [
    "DPP4",
    "COL1A1",
    "COL1A2",
    "COL3A1",
    "CTGF",
    "CTHRC1",
    "PRSS23",
    "THBS1",
    "FNDC1",
    "SFRP2",
    "SFRP4",
    "ACTA2",
    "TAGLN",
]

g = genes[genes["gene"].isin(genes_of_interest)].copy()

for col in ["delta_log_expression", "q_BH"]:
    g[col] = pd.to_numeric(g[col], errors="coerce")

g["significant"] = g["q_BH"] < 0.05

# keep the same visual order as the previous version
g["gene"] = pd.Categorical(
    g["gene"],
    categories=genes_of_interest[::-1],
    ordered=True
)
g = g.sort_values("gene")

sig = g[g["significant"]].copy()
ns = g[~g["significant"]].copy()

# ============================================================
# PANEL B — TOP REACTOME PATHWAYS
# ============================================================

r = reactome.copy()

for col in ["NES", "FDR_q"]:
    r[col] = pd.to_numeric(r[col], errors="coerce")

r_up = (
    r[
        (r["direction"] == "SSc_up")
        &
        (r["FDR_q"] < 0.05)
    ]
    .sort_values("NES", ascending=False)
    .head(10)
    .copy()
)

# reverse for top-to-bottom plotting
r_up = r_up.iloc[::-1].copy()

# shorten long pathway labels a bit
def shorten_label(x, max_len=46):
    """Truncate a label to a maximum length, appending ``"..."``.

    Parameters
    ----------
    x : object
        Label; converted to ``str``.
    max_len : int, default 46
        Maximum length of the returned string.

    Returns
    -------
    str
        The label, truncated if longer than ``max_len``.
    """
    x = str(x)
    return x if len(x) <= max_len else x[:max_len-3] + "..."

r_up["pathway_label"] = r_up["pathway_name"].map(shorten_label)

# ============================================================
# FIGURE LAYOUT — SAME STYLE, BETTER SPACING
# ============================================================

fig = make_subplots(
    rows=1,
    cols=2,
    horizontal_spacing=0.20,
    column_widths=[0.42, 0.58],
    subplot_titles=(
        "Fibrotic genes in SSc skin",
        "Top Reactome pathways increased in SSc"
    )
)

# ============================================================
# LEFT PANEL — GENE-LEVEL EFFECTS
# ============================================================

# significant
fig.add_trace(
    go.Scatter(
        x=sig["delta_log_expression"],
        y=sig["gene"],
        mode="markers",
        name="FDR < 0.05",
        marker=dict(
            size=9,
            color="royalblue",
            line=dict(width=0.6, color="royalblue")
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "SSc − control: %{x:.3f}<br>"
            "<extra></extra>"
        )
    ),
    row=1, col=1
)

# non-significant
if len(ns) > 0:
    fig.add_trace(
        go.Scatter(
            x=ns["delta_log_expression"],
            y=ns["gene"],
            mode="markers",
            name="Not significant",
            marker=dict(
                size=9,
                color="tomato",
                line=dict(width=0.6, color="tomato")
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "SSc − control: %{x:.3f}<br>"
                "<extra></extra>"
            )
        ),
        row=1, col=1
    )

# zero line
fig.add_vline(
    x=0,
    line_width=1,
    line_dash="dash",
    line_color="gray",
    row=1,
    col=1
)

# ============================================================
# RIGHT PANEL — PATHWAY-LEVEL ENRICHMENT
# ============================================================

fig.add_trace(
    go.Bar(
        x=r_up["NES"],
        y=r_up["pathway_label"],
        orientation="h",
        name="Reactome",
        marker=dict(
            color="#18c59c"
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "NES: %{x:.2f}<br>"
            "<extra></extra>"
        ),
        showlegend=True
    ),
    row=1, col=2
)

# ============================================================
# AXES
# ============================================================

fig.update_xaxes(
    title_text="SSc − control expression",
    row=1,
    col=1,
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",
    zeroline=False
)

fig.update_yaxes(
    title_text="",
    row=1,
    col=1,
    automargin=True
)

fig.update_xaxes(
    title_text="Normalized enrichment score (NES)",
    row=1,
    col=2,
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",
    zeroline=False
)

fig.update_yaxes(
    title_text="",
    row=1,
    col=2,
    automargin=True
)

# ============================================================
# TITLES / STYLING
# ============================================================

fig.update_layout(
    width=1450,
    height=620,
    template="plotly_white",
    title=dict(
        text=(
            "<b>Human systemic sclerosis skin is molecularly fibrotic</b>"
            "<br><sup>Patient transcriptomics independently converge on collagen and extracellular-matrix remodeling</sup>"
        ),
        x=0.5,
        xanchor="center"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.04,
        xanchor="left",
        x=0.0
    ),
    margin=dict(l=70, r=60, t=110, b=80)
)

# ============================================================
# SHOW
# ============================================================

fig.show()

# optional export
out_png = "/content/Figure_04_Human_SSc_fibrotic_program.png"
try:
    fig.write_image(out_png, scale=2)
    print(f"Saved figure to: {out_png}")
except Exception as e:
    print("Static export skipped:", e)

# ============================================================
# RESULT SUMMARY
# ============================================================

n_total = len(g)
n_sig_up = int(((g["delta_log_expression"] > 0) & (g["q_BH"] < 0.05)).sum())

dpp4_row = g[g["gene"] == "DPP4"]
if len(dpp4_row) == 1:
    dpp4_delta = float(dpp4_row["delta_log_expression"].iloc[0])
    dpp4_q = float(dpp4_row["q_BH"].iloc[0])
else:
    dpp4_delta = np.nan
    dpp4_q = np.nan

display(
    HTML(
        f"""
        <div style="border-left:4px solid #666; padding:12px 16px; margin-top:14px; line-height:1.6;">
        <b>Result</b><br>
        <b>{n_sig_up} of {n_total}</b> pre-specified genes are significantly increased in SSc skin, with strong convergence on collagen/ECM pathways.<br><br>
        <b>DPP4 behaves differently:</b> Δ expression = <b>{dpp4_delta:.3f}</b>, FDR = <b>{dpp4_q:.3g}</b>. It is therefore <b>not globally increased</b> in SSc skin.<br><br>
        <b>Verdict:</b> <b>HUMAN FIBROTIC DISEASE CONTEXT — SUPPORTED</b>
        </div>
        """
    )
)

# @title 5. DPP4 localizes to a fibroblast-relevant compartment in human skin {display-mode: "form"}
# @markdown **Question:** If DPP4 is not globally increased in SSc skin, which cell compartments express it?
# @markdown
# @markdown **Data:** GSE138669 human skin single-cell RNA-seq
# @markdown **Analysis:** Cell-type annotation + DPP4 single-cell expression
# @markdown **Analysis tools:** Scanpy · AnnData · Harmony representation
# @markdown **Visualization:** DaVinci UMAP outputs + Matplotlib descriptive summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image as PILImage
from IPython.display import display, HTML
from pathlib import Path


# ============================================================
# LOAD PROCESSED DAVINCI RESULTS
# ============================================================

celltype_dpp4 = load_tsv(
    "R2b_DPP4_celltype_descriptive_summary.tsv"
)


# ============================================================
# IMAGE PREPARATION
#
# The UMAPs were calculated and rendered previously on DaVinci.
# Here we only crop unused white margins and enlarge the raster
# for clearer notebook/presentation display.
# ============================================================

def crop_white_margin(
    image,
    threshold=248,
    padding=8,
):
    """Crop near-white margins from an image.

    Parameters
    ----------
    image : PIL.Image.Image
        Input image; converted to RGB first.
    threshold : int, default 248
        Pixels with any channel below this value count as content.
    padding : int, default 8
        Pixels of margin kept around the detected content.

    Returns
    -------
    PIL.Image.Image
        Cropped RGB image, or the RGB-converted input if it is entirely
        near-white.
    """
    img = image.convert("RGB")
    arr = np.asarray(img)

    # Identify pixels that are not near-white.
    mask = np.any(
        arr < threshold,
        axis=2
    )

    coords = np.argwhere(mask)

    if coords.size == 0:
        return img

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)

    x0 = max(
        0,
        x0 - padding
    )

    y0 = max(
        0,
        y0 - padding
    )

    x1 = min(
        img.width,
        x1 + padding
    )

    y1 = min(
        img.height,
        y1 + padding
    )

    return img.crop(
        (
            x0,
            y0,
            x1,
            y1,
        )
    )


def upscale_image(
    image,
    factor=2,
):
    """Upscale an image for display quality only.

    This does not create new biological information.

    Parameters
    ----------
    image : PIL.Image.Image
        Image to enlarge.
    factor : int, default 2
        Integer scale factor applied to width and height.

    Returns
    -------
    PIL.Image.Image
        Image resized with Lanczos resampling.
    """

    return image.resize(
        (
            image.width * factor,
            image.height * factor,
        ),
        PILImage.Resampling.LANCZOS,
    )


celltype_img = PILImage.open(
    data_file(
        "R2b_UMAP_celltypes.png"
    )
)

dpp4_img = PILImage.open(
    data_file(
        "R2b_UMAP_DPP4.png"
    )
)


celltype_img = upscale_image(
    crop_white_margin(
        celltype_img
    ),
    factor=2,
)

dpp4_img = upscale_image(
    crop_white_margin(
        dpp4_img
    ),
    factor=2,
)


# ============================================================
# DESCRIPTIVE CELL-TYPE SUMMARY
#
# Original results are stratified by condition and chemistry.
# Chemistry strata are collapsed descriptively within condition.
#
# This is NOT the formal donor-level disease test.
# ============================================================

summary = (
    celltype_dpp4
    .groupby(
        [
            "cell_type",
            "condition",
        ],
        as_index=False,
    )
    .agg(
        median_DPP4_positive=(
            "median_fraction_DPP4_positive",
            "median",
        ),

        median_DPP4_expression=(
            "median_DPP4_logexpr",
            "median",
        ),

        cells=(
            "total_cells",
            "sum",
        ),
    )
)


summary[
    "DPP4_positive_percent"
] = (
    summary[
        "median_DPP4_positive"
    ]
    * 100
)


# Order compartments by overall DPP4-positive fraction.
cell_order = (
    summary
    .groupby(
        "cell_type"
    )[
        "DPP4_positive_percent"
    ]
    .median()
    .sort_values(
        ascending=True
    )
    .index
    .tolist()
)


# ============================================================
# HIGH-RESOLUTION COMPOSITE FIGURE
#
# Layout:
#
# ┌──────────────────┬───────────────────────────────┐
# │ Cell landscape   │                               │
# │                  │ DPP4-positive fraction        │
# ├──────────────────┤                               │
# │ DPP4 expression  │                               │
# └──────────────────┴───────────────────────────────┘
#
# ============================================================

fig = plt.figure(
    figsize=(18, 10),
    dpi=150,
)


gs = fig.add_gridspec(
    nrows=2,
    ncols=2,

    width_ratios=[
        1.10,
        1.45,
    ],

    height_ratios=[
        1,
        1,
    ],

    left=0.04,
    right=0.98,
    top=0.88,
    bottom=0.08,

    wspace=0.20,
    hspace=0.20,
)


ax_cell = fig.add_subplot(
    gs[0, 0]
)

ax_dpp4 = fig.add_subplot(
    gs[1, 0]
)

ax_bar = fig.add_subplot(
    gs[:, 1]
)


# ============================================================
# PANEL A — CELLULAR LANDSCAPE
# ============================================================

ax_cell.imshow(
    celltype_img,
    interpolation="lanczos",
)

ax_cell.set_title(
    "Cellular landscape",
    fontsize=15,
    fontweight="bold",
    pad=10,
)

ax_cell.axis(
    "off"
)


# ============================================================
# PANEL B — DPP4 EXPRESSION
# ============================================================

ax_dpp4.imshow(
    dpp4_img,
    interpolation="lanczos",
)

ax_dpp4.set_title(
    "DPP4 expression",
    fontsize=15,
    fontweight="bold",
    pad=10,
)

ax_dpp4.axis(
    "off"
)


# ============================================================
# PANEL C — DPP4-POSITIVE CELLS BY COMPARTMENT
# ============================================================

conditions = (
    summary[
        "condition"
    ]
    .dropna()
    .unique()
    .tolist()
)


y = np.arange(
    len(
        cell_order
    )
)


n_conditions = len(
    conditions
)


# Side-by-side horizontal bars.
total_height = 0.70
bar_height = (
    total_height
    /
    max(
        n_conditions,
        1
    )
)


offsets = np.linspace(
    -total_height / 2 + bar_height / 2,
    total_height / 2 - bar_height / 2,
    n_conditions,
)


for offset, condition in zip(
    offsets,
    conditions,
):

    sub = (
        summary[
            summary[
                "condition"
            ]
            ==
            condition
        ]
        .set_index(
            "cell_type"
        )
        .reindex(
            cell_order
        )
    )

    values = (
        sub[
            "DPP4_positive_percent"
        ]
        .fillna(0)
        .values
    )

    ax_bar.barh(
        y + offset,
        values,
        height=bar_height,
        label=str(
            condition
        ),
    )


ax_bar.set_yticks(
    y
)

ax_bar.set_yticklabels(
    cell_order,
    fontsize=12,
)


ax_bar.set_xlabel(
    "Median fraction of DPP4-positive cells (%)",
    fontsize=12,
    labelpad=10,
)


ax_bar.set_title(
    "DPP4-positive cells by compartment",
    fontsize=15,
    fontweight="bold",
    pad=14,
)


ax_bar.grid(
    axis="x",
    alpha=0.20,
)


ax_bar.set_axisbelow(
    True
)


ax_bar.legend(
    frameon=False,
    loc="lower right",
    fontsize=11,
)


# Add some space beyond the longest bar.
max_value = (
    summary[
        "DPP4_positive_percent"
    ]
    .max()
)

ax_bar.set_xlim(
    0,
    max_value * 1.12
)


# Remove unnecessary borders.
ax_bar.spines[
    "top"
].set_visible(
    False
)

ax_bar.spines[
    "right"
].set_visible(
    False
)


# ============================================================
# MAIN TITLE
# ============================================================

fig.suptitle(
    "DPP4 shows a fibroblast-enriched distribution in human skin",
    fontsize=19,
    fontweight="bold",
    y=0.965,
)


fig.text(
    0.5,
    0.925,

    (
        "Single-cell localization in GSE138669 · "
        "descriptive cellular distribution"
    ),

    ha="center",
    fontsize=11,
)


# ============================================================
# EXPORT HIGH-RESOLUTION FIGURE
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_05_DPP4_cellular_localization.png"
)


fig.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight",
)


plt.show()


# ============================================================
# RESULT SUMMARY
# ============================================================

fib = (
    summary[
        summary[
            "cell_type"
        ]
        ==
        "Fibroblast"
    ]
)


if len(fib) > 0:

    fibroblast_range = (
        fib[
            "DPP4_positive_percent"
        ]
        .min(),
        fib[
            "DPP4_positive_percent"
        ]
        .max(),
    )

else:

    fibroblast_range = (
        np.nan,
        np.nan,
    )


display(
    HTML(
        f"""
        <div style="
            border-left:4px solid #777;
            padding:14px 18px;
            margin-top:12px;
            line-height:1.55;
        ">

        <b>Result</b><br>

        DPP4 is heterogeneously distributed across human skin and
        is most prominent in the <b>fibroblast compartment</b>.

        <br><br>

        Across the descriptive strata represented here,
        approximately
        <b>{fibroblast_range[0]:.1f}–{fibroblast_range[1]:.1f}%</b>
        of fibroblasts are DPP4-positive.

        <br><br>

        This supports a <b>cell-state model</b> rather than a
        requirement for whole-skin DPP4 overexpression.

        <br><br>

        <b>Important:</b>
        this panel is descriptive.
        Disease effects and DPP4–fibroblast-state relationships
        are tested using <b>donor-level inference</b> in the
        next analysis.

        <br><br>

        <b>Verdict:</b>
        CELLULAR LOCALIZATION —
        <b>SUPPORTED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 6. Independent human scRNA-seq replicates a state-linked DPP4 model {display-mode: "form"}
# @markdown **Question:** Within the fibroblast compartment, how does SSc alter fibroblast states, and which states remain associated with DPP4-positive fibroblasts?
# @markdown
# @markdown **Data:** GSE249279 independent human skin single-cell RNA-seq
# @markdown **Analysis:** donor-level fibroblast state scoring + robust regression
# @markdown **Analysis tools:** Python · Scanpy · AnnData · statsmodels
# @markdown **Visualization:** Matplotlib

# ============================================================
# BUILD FIGURE — PITCH-OPTIMIZED LAYOUT
# ============================================================

from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

fig = plt.figure(
    figsize=(15.5, 8.6),
    facecolor="white"
)

# ------------------------------------------------------------
# Dedicated rows:
#   1 = title/subtitle
#   2 = actual plots
#   3 = interpretation + legend
# ------------------------------------------------------------

gs = GridSpec(
    nrows=3,
    ncols=2,
    figure=fig,
    height_ratios=[0.13, 0.72, 0.15],
    width_ratios=[1, 1],
    hspace=0.28,
    wspace=0.48,
)

ax_header = fig.add_subplot(gs[0, :])
ax_a = fig.add_subplot(gs[1, 0])
ax_b = fig.add_subplot(gs[1, 1])
ax_footer = fig.add_subplot(gs[2, :])

ax_header.axis("off")
ax_footer.axis("off")


# ============================================================
# COLORS
# ============================================================

BLUE = "#2563EB"
GREEN = "#10B981"
RED = "#EF4444"
GRAY = "#CBD5E1"

TEXT = "#172033"
MUTED = "#64748B"
GRID = "#E5E7EB"


# ============================================================
# HEADER
# ============================================================

ax_header.text(
    0.5,
    0.72,
    "Independent human scRNA-seq replicates a state-linked DPP4 model",
    ha="center",
    va="center",
    fontsize=18,
    fontweight="bold",
    color=TEXT,
)

ax_header.text(
    0.5,
    0.28,
    (
        "SSc fibroblasts shift toward activated / ECM programs, "
        "while DPP4-positive fibroblasts remain linked to progenitor and ECM states"
    ),
    ha="center",
    va="center",
    fontsize=11.5,
    color=MUTED,
)


# ============================================================
# LABEL HELPER
# ============================================================

def compact_q(q):
    """Format a q-value as a compact plot label.

    Parameters
    ----------
    q : float or None
        FDR-adjusted q-value; missing values are allowed.

    Returns
    -------
    str
        ``"q = NA"``, ``"q < 0.001"``, or ``"q = <value>"``.
    """
    if pd.isna(q):
        return "q = NA"
    q = float(q)
    if q < 0.001:
        return "q < 0.001"
    if q < 0.01:
        return f"q = {q:.3f}"
    return f"q = {q:.2f}"


def annotate_bar(
    ax,
    value,
    y,
    q,
    bar_color,
    axis_span,
):
    """Write a beta / q-value label on a horizontal bar.

    Large bars (``|value| >= 0.55``) get the label inside the bar; small bars
    get it just outside the bar end.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes containing the bar.
    value : float
        Bar length (effect size, beta in SD units).
    y : float
        Bar position on the y axis.
    q : float
        FDR-adjusted q-value shown under the beta.
    bar_color : str
        Bar color; colored bars get white bold text when labeled inside.
    axis_span : float
        Width of the x axis, used to scale label offsets.
    """

    txt = (
        f"β = {value:.2f}\n"
        f"{compact_q(q)}"
    )

    # threshold relative to axis scale
    large_bar = abs(value) >= 0.55

    if large_bar:
        # Keep text INSIDE the bar
        if value > 0:
            x = value - axis_span * 0.025
            ha = "right"
        else:
            x = value + axis_span * 0.025
            ha = "left"

        # significant colored bars can take white text
        text_color = (
            "white"
            if bar_color in [BLUE, GREEN, RED]
            else TEXT
        )

        ax.text(
            x,
            y,
            txt,
            ha=ha,
            va="center",
            fontsize=9.0,
            color=text_color,
            fontweight="bold" if text_color == "white" else "normal",
            linespacing=1.15,
        )

    else:
        # Small bars: put annotation just outside endpoint
        offset = axis_span * 0.018

        if value >= 0:
            x = value + offset
            ha = "left"
        else:
            x = value - offset
            ha = "right"

        ax.text(
            x,
            y,
            txt,
            ha=ha,
            va="center",
            fontsize=8.7,
            color=TEXT,
            linespacing=1.15,
        )


# NOTE: `d` (beta_SSc_SD, q_BH, color, label) and `a` (beta_exposure_SD,
# q_BH, color, label) are not defined earlier in this file. The cell that
# built them is missing from the Colab export, so running top to bottom
# raises NameError here. Figure 6's values cannot be traced in this repo.

# ============================================================
# PANEL A — DISEASE EFFECT
# ============================================================

y_a = np.arange(len(d))

ax_a.barh(
    y_a,
    d["beta_SSc_SD"],
    color=d["color"],
    height=0.62,
    edgecolor="none",
)

ax_a.axvline(
    0,
    color="#94A3B8",
    linestyle="--",
    linewidth=1.1,
)

ax_a.set_yticks(y_a)
ax_a.set_yticklabels(
    d["label"],
    fontsize=10.5,
)

ax_a.invert_yaxis()

# Extra room prevents annotations from touching labels
ax_a.set_xlim(-2.75, 2.05)

ax_a.set_xlabel(
    "SSc effect size (β SD)",
    fontsize=10.5,
    labelpad=8,
)

ax_a.set_title(
    "A  What changes in SSc fibroblasts?",
    loc="left",
    fontsize=13,
    fontweight="bold",
    pad=20,
    color=TEXT,
)

ax_a.text(
    0.0,
    1.025,
    "Positive = higher in SSc     |     Negative = lower in SSc",
    transform=ax_a.transAxes,
    ha="left",
    va="bottom",
    fontsize=9.2,
    color=MUTED,
)

ax_a.grid(
    axis="x",
    color=GRID,
    linewidth=0.8,
)

ax_a.set_axisbelow(True)

# remove unnecessary frame
ax_a.spines["top"].set_visible(False)
ax_a.spines["right"].set_visible(False)

span_a = ax_a.get_xlim()[1] - ax_a.get_xlim()[0]

for i, row in d.iterrows():

    annotate_bar(
        ax=ax_a,
        value=float(row["beta_SSc_SD"]),
        y=i,
        q=row["q_BH"],
        bar_color=row["color"],
        axis_span=span_a,
    )


# ============================================================
# PANEL B — DPP4 STATE COUPLING
# ============================================================

y_b = np.arange(len(a))

ax_b.barh(
    y_b,
    a["beta_exposure_SD"],
    color=a["color"],
    height=0.62,
    edgecolor="none",
)

ax_b.axvline(
    0,
    color="#94A3B8",
    linestyle="--",
    linewidth=1.1,
)

ax_b.set_yticks(y_b)
ax_b.set_yticklabels(
    a["label"],
    fontsize=10.5,
)

ax_b.invert_yaxis()

ax_b.set_xlim(-1.35, 1.35)

ax_b.set_xlabel(
    "Association with DPP4-positive fraction (β SD)",
    fontsize=10.5,
    labelpad=8,
)

ax_b.set_title(
    "B  Which fibroblast states track DPP4 positivity?",
    loc="left",
    fontsize=13,
    fontweight="bold",
    pad=20,
    color=TEXT,
)

ax_b.text(
    0.0,
    1.025,
    "Positive = tracks DPP4+ fraction     |     Gray = not significant",
    transform=ax_b.transAxes,
    ha="left",
    va="bottom",
    fontsize=9.2,
    color=MUTED,
)

ax_b.grid(
    axis="x",
    color=GRID,
    linewidth=0.8,
)

ax_b.set_axisbelow(True)

ax_b.spines["top"].set_visible(False)
ax_b.spines["right"].set_visible(False)

span_b = ax_b.get_xlim()[1] - ax_b.get_xlim()[0]

for i, row in a.iterrows():

    annotate_bar(
        ax=ax_b,
        value=float(row["beta_exposure_SD"]),
        y=i,
        q=row["q_BH"],
        bar_color=row["color"],
        axis_span=span_b,
    )


# ============================================================
# FOOTER — INTERPRETATION
# ============================================================

ax_footer.text(
    0.5,
    0.72,
    (
        "DPP4 abundance decreases overall in SSc fibroblasts, "
        "but DPP4-positive fibroblasts remain specifically associated "
        "with progenitor and ECM programs."
    ),
    ha="center",
    va="center",
    fontsize=11.2,
    color=TEXT,
    fontweight="bold",
)

ax_footer.text(
    0.5,
    0.42,
    (
        "Take-home: DPP4 behaves as a fibroblast-state marker, "
        "not as a simple whole-compartment overexpression marker."
    ),
    ha="center",
    va="center",
    fontsize=10.6,
    color=MUTED,
    style="italic",
)


# ============================================================
# COMPACT LEGEND
# ============================================================

legend_handles = [

    Patch(
        facecolor=BLUE,
        label="Higher in SSc",
    ),

    Patch(
        facecolor=RED,
        label="Lower in SSc",
    ),

    Patch(
        facecolor=GREEN,
        label="Positive DPP4-state association",
    ),

    Patch(
        facecolor=GRAY,
        label="Not significant",
    ),
]

ax_footer.legend(
    handles=legend_handles,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.03),
    ncol=4,
    frameon=False,
    fontsize=9.3,
    columnspacing=2.2,
    handlelength=1.7,
)


# ============================================================
# FINAL SPACING
# ============================================================

fig.subplots_adjust(
    left=0.14,
    right=0.97,
    top=0.97,
    bottom=0.055,
)


# ============================================================
# EXPORT
# ============================================================

out_png = (
    "/content/"
    "Figure_06_Independent_scRNA_visual_summary_final.png"
)

fig.savefig(
    out_png,
    dpi=300,
    bbox_inches="tight",
    facecolor="white",
)

plt.show()

print(
    f"High-resolution figure saved to:\n{out_png}"
)

## @title 7. Fibroblast-state organization is branch-aware {display-mode: "form"}
# @markdown **Question:** Does the published DPP4/SFRP2 progenitor model behave as one obligatory fibrotic trajectory, or as part of a broader branch-aware fibroblast organization?
# @markdown
# @markdown **Data:** GSE138669 human skin fibroblast single-cell RNA-seq
# @markdown **Analysis:** fibroblast graph reconstruction + PAGA topology + donor-level disease-state occupancy
# @markdown **Analysis tools:** Scanpy · Harmony · PAGA · NetworkX · statsmodels
# @markdown **Literature anchor:** Tabib et al., *Nature Communications* (2021) · PMID 34282151
# @markdown **Visualization:** single integrated PAGA network · Matplotlib
# @markdown
# @markdown **How to read:** network structure represents PAGA connectivity; node color represents the adjusted SSc effect on donor-level cluster occupancy. Red = enriched in SSc; blue = depleted in SSc.

import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from PIL import Image
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch
from IPython.display import display, HTML


# ============================================================
# INPUT
#
# Use the disease-enrichment PAGA graph as the single network.
# The topology is identical to the state graph; therefore,
# there is no need to show the same network twice.
# ============================================================

img_enrichment = data_file(
    "R9b_PAGA_SSc_enrichment.png"
)

network_img = Image.open(
    img_enrichment
).convert("RGB")


# ============================================================
# CROP WHITE MARGINS
# ============================================================

def crop_white_margin(
    image,
    threshold=248,
    padding=10,
):
    """Crop near-white margins from an RGB image.

    Parameters
    ----------
    image : PIL.Image.Image
        RGB image (a 3-channel array is assumed).
    threshold : int, default 248
        Pixels with any channel below this value count as content.
    padding : int, default 10
        Pixels of margin kept around the detected content.

    Returns
    -------
    PIL.Image.Image
        Cropped image, or the input unchanged if it is entirely near-white.
    """

    arr = np.asarray(
        image
    )

    mask = np.any(
        arr < threshold,
        axis=2,
    )

    coords = np.argwhere(
        mask
    )

    if coords.size == 0:
        return image

    y0, x0 = coords.min(
        axis=0
    )

    y1, x1 = coords.max(
        axis=0
    )

    x0 = max(
        0,
        x0 - padding
    )

    y0 = max(
        0,
        y0 - padding
    )

    x1 = min(
        image.width,
        x1 + padding
    )

    y1 = min(
        image.height,
        y1 + padding
    )

    return image.crop(
        (
            x0,
            y0,
            x1,
            y1,
        )
    )


network_img = crop_white_margin(
    network_img
)


# ============================================================
# COLORS
# ============================================================

TEXT = "#172033"
MUTED = "#64748B"

DPP4_COLOR = "#218C5A"
MYO_COLOR = "#8064A2"
SSC_COLOR = "#C94B4B"

SOFT_GREEN = "#EEF8F2"
SOFT_PURPLE = "#F4F1FA"
SOFT_RED = "#FCF0EF"

BORDER = "#D7DEE5"
SOFT_GRAY = "#F7F9FB"


# ============================================================
# FIGURE LAYOUT
#
# One network + interpretation panel.
# ============================================================

fig = plt.figure(
    figsize=(14.8, 7.5),
    dpi=180,
    facecolor="white",
)


gs = GridSpec(
    nrows=3,
    ncols=2,
    figure=fig,

    height_ratios=[
        0.14,
        0.72,
        0.14,
    ],

    width_ratios=[
        1.55,
        0.45,
    ],

    hspace=0.22,
    wspace=0.12,
)


ax_header = fig.add_subplot(
    gs[0, :]
)

ax_network = fig.add_subplot(
    gs[1, 0]
)

ax_info = fig.add_subplot(
    gs[1, 1]
)

ax_footer = fig.add_subplot(
    gs[2, :]
)


ax_header.axis("off")
ax_network.axis("off")
ax_info.axis("off")
ax_footer.axis("off")


# ============================================================
# HEADER
# ============================================================

ax_header.text(
    0.5,
    0.73,

    "Human SSc fibroblast organization is branch-aware",

    ha="center",
    va="center",

    fontsize=18,
    fontweight="bold",

    color=TEXT,
)


ax_header.text(
    0.5,
    0.27,

    (
        "The published DPP4/SFRP2 progenitor model is compatible with "
        "a broader non-linear fibroblast topology"
    ),

    ha="center",
    va="center",

    fontsize=11.3,

    color=MUTED,
)


# ============================================================
# MAIN NETWORK
# ============================================================

ax_network.imshow(
    network_img,
    interpolation="lanczos",
)


ax_network.axis(
    "off"
)


ax_network.set_title(
    "Integrated fibroblast topology and SSc state occupancy",

    fontsize=13,

    fontweight="bold",

    pad=10,

    color=TEXT,
)


# ============================================================
# INFORMATION PANEL
# ============================================================

panel = FancyBboxPatch(
    (
        0.03,
        0.04
    ),

    0.94,
    0.92,

    boxstyle=(
        "round,pad=0.018,"
        "rounding_size=0.025"
    ),

    transform=ax_info.transAxes,

    facecolor=SOFT_GRAY,

    edgecolor=BORDER,

    linewidth=1.2,
)


ax_info.add_patch(
    panel
)


# ============================================================
# HOW TO READ
# ============================================================

ax_info.text(
    0.10,
    0.90,

    "How to read the network",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=11.8,

    fontweight="bold",

    color=TEXT,
)


ax_info.text(
    0.10,
    0.835,

    (
        "Node color = SSc occupancy effect\n"
        "Red = enriched in SSc\n"
        "Blue = depleted in SSc\n"
        "Edges = PAGA state connectivity"
    ),

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=9.1,

    color=MUTED,

    linespacing=1.45,
)


# ============================================================
# BRANCH 1
# ============================================================

box1 = FancyBboxPatch(
    (
        0.08,
        0.545
    ),

    0.84,
    0.19,

    boxstyle=(
        "round,pad=0.012,"
        "rounding_size=0.020"
    ),

    transform=ax_info.transAxes,

    facecolor=SOFT_GREEN,

    edgecolor=DPP4_COLOR,

    linewidth=1.3,
)


ax_info.add_patch(
    box1
)


ax_info.text(
    0.12,
    0.695,

    "DPP4-associated branch",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=10.8,

    fontweight="bold",

    color=DPP4_COLOR,
)


ax_info.text(
    0.12,
    0.635,

    "0  →  2  →  4",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=12,

    fontweight="bold",

    color=TEXT,
)


ax_info.text(
    0.12,
    0.585,

    (
        "DPP4-high / activated / ECM-related\n"
        "organization shares this route."
    ),

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=8.9,

    color=TEXT,

    linespacing=1.3,
)


# ============================================================
# BRANCH 2
# ============================================================

box2 = FancyBboxPatch(
    (
        0.08,
        0.325
    ),

    0.84,
    0.17,

    boxstyle=(
        "round,pad=0.012,"
        "rounding_size=0.020"
    ),

    transform=ax_info.transAxes,

    facecolor=SOFT_PURPLE,

    edgecolor=MYO_COLOR,

    linewidth=1.3,
)


ax_info.add_patch(
    box2
)


ax_info.text(
    0.12,
    0.455,

    "Partially distinct route",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=10.8,

    fontweight="bold",

    color=MYO_COLOR,
)


ax_info.text(
    0.12,
    0.400,

    "0  →  6  →  9",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=12,

    fontweight="bold",

    color=TEXT,
)


ax_info.text(
    0.12,
    0.350,

    "Myofibroblast-high state",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=8.9,

    color=TEXT,
)


# ============================================================
# DISEASE OCCUPANCY
# ============================================================

box3 = FancyBboxPatch(
    (
        0.08,
        0.115
    ),

    0.84,
    0.16,

    boxstyle=(
        "round,pad=0.012,"
        "rounding_size=0.020"
    ),

    transform=ax_info.transAxes,

    facecolor=SOFT_RED,

    edgecolor=SSC_COLOR,

    linewidth=1.3,
)


ax_info.add_patch(
    box3
)


ax_info.text(
    0.12,
    0.235,

    "Disease remodeling",

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=10.8,

    fontweight="bold",

    color=SSC_COLOR,
)


ax_info.text(
    0.12,
    0.180,

    (
        "SSc preferentially enriches selected\n"
        "states rather than uniformly expanding\n"
        "the entire fibroblast graph."
    ),

    transform=ax_info.transAxes,

    ha="left",
    va="top",

    fontsize=8.8,

    color=TEXT,

    linespacing=1.3,
)


# ============================================================
# FOOTER — TAKE-HOME
# ============================================================

ax_footer.text(
    0.5,
    0.68,

    (
        "Take-home: DPP4-associated fibroblast states belong to a "
        "disease-relevant branch, but they do not define a single obligatory "
        "trajectory toward every fibrotic endpoint."
    ),

    ha="center",
    va="center",

    fontsize=11.2,

    fontweight="bold",

    color=TEXT,
)


ax_footer.text(
    0.5,
    0.25,

    (
        "PAGA describes connectivity between cellular states; "
        "it does not by itself prove lineage direction or causal differentiation."
    ),

    ha="center",
    va="center",

    fontsize=9.5,

    color=MUTED,

    style="italic",
)


# ============================================================
# FINAL SPACING
# ============================================================

fig.subplots_adjust(
    left=0.035,
    right=0.985,
    top=0.97,
    bottom=0.04,
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_07_integrated_branch_aware_PAGA.png"
)


fig.savefig(
    OUTPUT_FIGURE,

    dpi=300,

    bbox_inches="tight",

    facecolor="white",
)


plt.show()


# ============================================================
# INTERPRETATION
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #218C5A;
            padding:14px 18px;
            margin-top:10px;
            line-height:1.55;
        ">

        <b>Result</b><br>

        The PAGA reconstruction is consistent with and refines the
        fibroblast organization previously described in human systemic
        sclerosis.

        <br><br>

        Tabib et al. identified
        <b>SFRP2<sup>hi</sup>/DPP4-expressing fibroblasts as a
        progenitor-like population capable of contributing to
        fibrogenic differentiation</b>
        (Nature Communications, 2021; PMID 34282151).

        <br><br>

        Consistent with this biological framework, our reconstruction
        does <b>not</b> support one obligatory
        DPP4 → activated → myofibroblast → ECM sequence.

        Instead:

        <ul style="
            margin-top:8px;
            margin-bottom:8px;
        ">

          <li>
            DPP4-high, activated and ECM-associated organization
            shares the <b>0 → 2 → 4 branch</b>.
          </li>

          <li>
            The myofibroblast-high state occupies a
            <b>partially distinct 0 → 6 → 9 route</b>.
          </li>

          <li>
            SSc modifies occupancy of selected regions of this topology,
            rather than uniformly expanding all fibroblast states.
          </li>

        </ul>

        <b>Interpretation:</b><br>

        Our analysis therefore
        <b>supports and refines the published DPP4/SFRP2 progenitor model</b>.

        DPP4 is better interpreted as identifying a
        <b>disease-relevant fibroblast branch/state context</b>,
        rather than as a universal marker of a single terminal
        myofibroblast trajectory.

        <br><br>

        <b>Important:</b><br>

        PAGA estimates topological connectivity between cellular states.
        It does not by itself demonstrate lineage direction,
        temporal progression or causality.

        <br><br>

        <b>Verdict:</b><br>

        PUBLISHED DPP4/SFRP2 PROGENITOR MODEL —
        <b>SUPPORTED AND REFINED</b><br>

        BRANCH-AWARE FIBROBLAST ORGANIZATION —
        <b>SUPPORTED</b><br>

        SINGLE OBLIGATORY DPP4 → MYOFIBROBLAST → ECM TRAJECTORY —
        <b>NOT SUPPORTED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 8. DPP4-positive fibroblasts occupy a distinct regulatory state {display-mode: "form"}
# @markdown **Question:** Is the DPP4-positive fibroblast state the one with maximal canonical profibrotic signaling?
# @markdown
# @markdown **Data:** GSE138669 + GSE249279 human skin fibroblast pseudobulk
# @markdown **Analysis:** pathway and transcription-factor activity inference
# @markdown **Analysis tools:** decoupler · PROGENy · CollecTRI · ULM · paired donor-level comparison
# @markdown **Replication:** two independent human SSc single-cell cohorts
# @markdown **Visualization:** Matplotlib
# @markdown
# @markdown **How to read the figure:** color and symbol identify the independent human cohort; filled markers indicate q < 0.05; open markers indicate q ≥ 0.05. In Panel A, horizontal lines represent 95% confidence intervals.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# LOAD RESULTS
# ============================================================

disease = load_tsv(
    "R12_disease_regulatory_activity.tsv"
)

replication = load_tsv(
    "R12_cross_cohort_replication.tsv"
)


# ============================================================
# COLUMN HELPERS
# ============================================================

def first_existing(df, candidates):
    """Return the first candidate column present in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Table to search.
    candidates : list of str
        Column names in order of preference.

    Returns
    -------
    str
        The first name in ``candidates`` that is a column of ``df``.

    Raises
    ------
    KeyError
        If none of the candidates is present.
    """

    for column in candidates:

        if column in df.columns:
            return column

    raise KeyError(
        "Missing expected columns: "
        + ", ".join(candidates)
    )


disease_effect_col = first_existing(
    disease,
    [
        "beta_SSc",
        "beta_SSc_SD",
        "beta",
        "effect",
    ]
)

disease_ci_low_col = first_existing(
    disease,
    [
        "CI_low",
        "ci_low",
    ]
)

disease_ci_high_col = first_existing(
    disease,
    [
        "CI_high",
        "ci_high",
    ]
)

disease_q_col = first_existing(
    disease,
    [
        "q_BH",
        "q",
        "FDR",
    ]
)


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for column in [
    disease_effect_col,
    disease_ci_low_col,
    disease_ci_high_col,
    disease_q_col,
]:

    disease[column] = pd.to_numeric(
        disease[column],
        errors="coerce",
    )


for column in [
    "R2_mean_delta",
    "R11_mean_delta",
    "R2_q",
    "R11_q",
    "meta_q",
]:

    if column in replication.columns:

        replication[column] = pd.to_numeric(
            replication[column],
            errors="coerce",
        )


# ============================================================
# PANEL A DATA
# Disease-wide TGFβ / SMAD activity
# ============================================================

targets = [
    "TGFb",
    "SMAD2",
    "SMAD3",
    "SMAD4",
]


d = (
    disease[
        disease[
            "regulator"
        ].isin(
            targets
        )
    ]
    .copy()
)


# ============================================================
# PANEL B DATA
# DPP4+ vs DPP4− regulatory activity
# ============================================================

pathways = [
    "TGFb",
    "MAPK",
    "NFkB",
    "JAK-STAT",
    "PI3K",
]


r = (
    replication[
        (
            replication[
                "family"
            ]
            ==
            "Pathway"
        )
        &
        (
            replication[
                "regulator"
            ].isin(
                pathways
            )
        )
    ]
    .copy()
)


# ============================================================
# DISPLAY LABELS
# ============================================================

COHORTS = {

    "R2": {
        "label": "GSE138669",
        "color": "#2563EB",
        "marker": "o",
    },

    "R11": {
        "label": "GSE249279",
        "color": "#F97316",
        "marker": "s",
    },
}


REGULATOR_LABELS = {

    "TGFb": "TGFβ",

    "SMAD2": "SMAD2",

    "SMAD3": "SMAD3",

    "SMAD4": "SMAD4",

    "MAPK": "MAPK",

    "NFkB": "NFκB",

    "JAK-STAT": "JAK–STAT",

    "PI3K": "PI3K",
}


# ============================================================
# BIOLOGICAL ORDER
# ============================================================

reg_order_A = [
    "TGFb",
    "SMAD2",
    "SMAD3",
    "SMAD4",
]


pathway_order_B = [
    "TGFb",
    "MAPK",
    "NFkB",
    "JAK-STAT",
    "PI3K",
]


# ============================================================
# FIGURE LAYOUT
#
# Dedicated rows:
#   1 = title / subtitle
#   2 = plots
#   3 = legend / interpretation
# ============================================================

fig = plt.figure(
    figsize=(14.8, 7.8),
    dpi=180,
    facecolor="white",
)


gs = GridSpec(
    nrows=3,
    ncols=2,
    figure=fig,

    height_ratios=[
        0.13,
        0.73,
        0.14,
    ],

    width_ratios=[
        1,
        1,
    ],

    hspace=0.27,
    wspace=0.38,
)


ax_header = fig.add_subplot(
    gs[0, :]
)

ax1 = fig.add_subplot(
    gs[1, 0]
)

ax2 = fig.add_subplot(
    gs[1, 1]
)

ax_footer = fig.add_subplot(
    gs[2, :]
)


ax_header.axis(
    "off"
)

ax_footer.axis(
    "off"
)


# ============================================================
# HEADER
# ============================================================

ax_header.text(
    0.5,
    0.72,

    "DPP4-positive fibroblasts occupy a distinct regulatory state",

    ha="center",
    va="center",

    fontsize=18,
    fontweight="bold",

    color="#172033",
)


ax_header.text(
    0.5,
    0.27,

    (
        "Two independent human cohorts replicate disease-wide TGFβ/SMAD activation, "
        "but DPP4-positive fibroblasts show a distinct signaling profile"
    ),

    ha="center",
    va="center",

    fontsize=11.2,

    color="#64748B",
)


# ============================================================
# PANEL A
# Is the SSc fibroblast environment TGFβ / SMAD active?
# ============================================================

y_base_A = {

    regulator:
        len(reg_order_A) - 1 - i

    for i, regulator
    in enumerate(
        reg_order_A
    )
}


cohort_offset = {

    "R2":
        +0.09,

    "R11":
        -0.09,
}


for cohort in [
    "R2",
    "R11",
]:

    sub = d[
        d[
            "cohort"
        ].astype(str)
        ==
        cohort
    ].copy()


    for _, row in sub.iterrows():

        regulator = str(
            row[
                "regulator"
            ]
        )


        if regulator not in y_base_A:
            continue


        effect = float(
            row[
                disease_effect_col
            ]
        )


        ci_low = float(
            row[
                disease_ci_low_col
            ]
        )


        ci_high = float(
            row[
                disease_ci_high_col
            ]
        )


        q = float(
            row[
                disease_q_col
            ]
        )


        significant = (
            q < 0.05
        )


        y = (
            y_base_A[
                regulator
            ]
            +
            cohort_offset[
                cohort
            ]
        )


        color = COHORTS[
            cohort
        ][
            "color"
        ]


        marker = COHORTS[
            cohort
        ][
            "marker"
        ]


        ax1.errorbar(
            effect,
            y,

            xerr=np.array(
                [
                    [
                        effect
                        -
                        ci_low
                    ],
                    [
                        ci_high
                        -
                        effect
                    ],
                ]
            ),

            fmt=marker,

            markersize=7.5,

            markerfacecolor=(
                color
                if significant
                else
                "white"
            ),

            markeredgecolor=color,

            markeredgewidth=1.5,

            ecolor=color,

            elinewidth=1.35,

            capsize=0,

            alpha=(
                1.0
                if significant
                else
                0.55
            ),

            zorder=3,
        )


ax1.axvline(
    0,

    linestyle="--",

    linewidth=1.1,

    color="#94A3B8",
)


ax1.set_yticks(
    [
        y_base_A[
            regulator
        ]
        for regulator
        in reg_order_A
    ]
)


ax1.set_yticklabels(
    [
        REGULATOR_LABELS[
            regulator
        ]
        for regulator
        in reg_order_A
    ],

    fontsize=11,
)


ax1.set_xlabel(
    "SSc − control inferred activity",

    fontsize=10.5,

    labelpad=8,
)


ax1.set_title(
    "A  Is the SSc fibroblast environment TGFβ/SMAD-active?",

    loc="left",

    fontsize=12.5,

    fontweight="bold",

    pad=18,
)


ax1.text(
    0.0,
    1.015,

    "Right of zero = higher inferred activity in SSc",

    transform=ax1.transAxes,

    fontsize=9.2,

    color="#64748B",

    ha="left",
    va="bottom",
)


ax1.grid(
    axis="x",

    alpha=0.15,
)


ax1.set_axisbelow(
    True
)


ax1.spines[
    "top"
].set_visible(
    False
)


ax1.spines[
    "right"
].set_visible(
    False
)


# ============================================================
# PANEL B
# Is DPP4+ the state with maximal canonical signaling?
# ============================================================

y_base_B = {

    pathway:
        len(pathway_order_B) - 1 - i

    for i, pathway
    in enumerate(
        pathway_order_B
    )
}


for _, row in r.iterrows():

    pathway = str(
        row[
            "regulator"
        ]
    )


    if pathway not in y_base_B:
        continue


    y0 = y_base_B[
        pathway
    ]


    x_r2 = float(
        row[
            "R2_mean_delta"
        ]
    )


    x_r11 = float(
        row[
            "R11_mean_delta"
        ]
    )


    # --------------------------------------------------------
    # Connector:
    # same pathway estimated in both independent cohorts
    # --------------------------------------------------------

    ax2.plot(
        [
            x_r2,
            x_r11,
        ],

        [
            y0 + 0.09,
            y0 - 0.09,
        ],

        color="#CBD5E1",

        linewidth=1.5,

        zorder=1,
    )


    for (
        cohort,
        x,
        q_col,
        y_offset,
    ) in [

        (
            "R2",
            x_r2,
            "R2_q",
            +0.09,
        ),

        (
            "R11",
            x_r11,
            "R11_q",
            -0.09,
        ),
    ]:

        q = float(
            row[
                q_col
            ]
        )


        significant = (
            q < 0.05
        )


        color = COHORTS[
            cohort
        ][
            "color"
        ]


        marker = COHORTS[
            cohort
        ][
            "marker"
        ]


        ax2.scatter(
            x,
            y0 + y_offset,

            s=62,

            marker=marker,

            facecolor=(
                color
                if significant
                else
                "white"
            ),

            edgecolor=color,

            linewidth=1.5,

            alpha=(
                1.0
                if significant
                else
                0.60
            ),

            zorder=4,
        )


ax2.axvline(
    0,

    linestyle="--",

    linewidth=1.1,

    color="#94A3B8",
)


ax2.set_yticks(
    [
        y_base_B[
            pathway
        ]
        for pathway
        in pathway_order_B
    ]
)


ax2.set_yticklabels(
    [
        REGULATOR_LABELS[
            pathway
        ]
        for pathway
        in pathway_order_B
    ],

    fontsize=11,
)


# ============================================================
# SYMMETRIC X-AXIS
# ============================================================

all_values = np.concatenate(
    [
        r[
            "R2_mean_delta"
        ].dropna().values,

        r[
            "R11_mean_delta"
        ].dropna().values,
    ]
)


absmax = max(
    np.abs(
        all_values
    ).max(),

    0.6,
)


ax2.set_xlim(
    -absmax * 1.22,

    absmax * 1.22,
)


ax2.set_xlabel(
    "DPP4+ − DPP4− inferred activity",

    fontsize=10.5,

    labelpad=8,
)


ax2.set_title(
    "B  Is DPP4+ the state with maximal canonical signaling?",

    loc="left",

    fontsize=12.5,

    fontweight="bold",

    pad=18,
)


# ============================================================
# DIRECTION LABELS
# ============================================================

ax2.text(
    0.01,
    1.015,

    "← lower in DPP4+",

    transform=ax2.transAxes,

    fontsize=9.2,

    color="#64748B",

    ha="left",
    va="bottom",
)


ax2.text(
    0.99,
    1.015,

    "higher in DPP4+ →",

    transform=ax2.transAxes,

    fontsize=9.2,

    color="#64748B",

    ha="right",
    va="bottom",
)


ax2.grid(
    axis="x",

    alpha=0.15,
)


ax2.set_axisbelow(
    True
)


ax2.spines[
    "top"
].set_visible(
    False
)


ax2.spines[
    "right"
].set_visible(
    False
)


# ============================================================
# LEGEND
# ============================================================

cohort_legend = [

    Line2D(
        [0],
        [0],

        marker="o",

        linestyle="None",

        markerfacecolor=COHORTS[
            "R2"
        ][
            "color"
        ],

        markeredgecolor=COHORTS[
            "R2"
        ][
            "color"
        ],

        markersize=8,

        label="GSE138669",
    ),


    Line2D(
        [0],
        [0],

        marker="s",

        linestyle="None",

        markerfacecolor=COHORTS[
            "R11"
        ][
            "color"
        ],

        markeredgecolor=COHORTS[
            "R11"
        ][
            "color"
        ],

        markersize=8,

        label="GSE249279",
    ),
]


# ============================================================
# FOOTER — HOW TO READ
# ============================================================

ax_footer.text(
    0.5,
    0.79,

    (
        "How to read: color + symbol = independent human cohort  ·  "
        "filled marker = q < 0.05  ·  open marker = q ≥ 0.05  ·  "
        "Panel A horizontal line = 95% CI"
    ),

    ha="center",
    va="center",

    fontsize=9.4,

    color="#475569",
)


ax_footer.legend(
    handles=cohort_legend,

    loc="center",

    bbox_to_anchor=(
        0.5,
        0.50
    ),

    ncol=2,

    frameon=False,

    fontsize=10,

    columnspacing=2.5,
)


ax_footer.text(
    0.5,
    0.16,

    (
        "Take-home: SSc-wide TGFβ/SMAD activation is replicated, "
        "but DPP4-positive fibroblasts represent a distinct regulatory state "
        "rather than the state with maximal canonical TGFβ signaling."
    ),

    ha="center",
    va="center",

    fontsize=10.6,

    fontweight="bold",

    color="#172033",
)


# ============================================================
# FINAL SPACING
# ============================================================

fig.subplots_adjust(
    left=0.10,

    right=0.98,

    top=0.97,

    bottom=0.04,
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_08_DPP4_regulatory_state_explained.png"
)


fig.savefig(
    OUTPUT_FIGURE,

    dpi=300,

    bbox_inches="tight",

    facecolor="white",
)


plt.show()


# ============================================================
# RESULT HELPERS
# ============================================================

def get_row(
    regulator
):
    """Return the cross-cohort replication row for one regulator.

    Reads the module-level table ``r`` built in this cell.

    Parameters
    ----------
    regulator : str
        Regulator/pathway name, e.g. ``"TGFb"``.

    Returns
    -------
    pandas.Series or None
        The first matching row, or ``None`` if absent.
    """

    x = r[
        r[
            "regulator"
        ].astype(str)
        ==
        regulator
    ]

    if len(x) == 0:
        return None

    return x.iloc[0]


def fmt_pair(
    row
):
    """Format DPP4+ minus DPP4- activity for both cohorts.

    Parameters
    ----------
    row : pandas.Series or None
        Row with ``R2_mean_delta`` and ``R11_mean_delta`` columns.

    Returns
    -------
    str
        ``"GSE138669 <x>; GSE249279 <y>"``, or ``"NA"`` if ``row`` is None.
    """

    if row is None:
        return "NA"

    return (
        f"GSE138669 {row['R2_mean_delta']:.2f}; "
        f"GSE249279 {row['R11_mean_delta']:.2f}"
    )


tgfb = get_row(
    "TGFb"
)

mapk = get_row(
    "MAPK"
)

nfkb = get_row(
    "NFkB"
)

jakstat = get_row(
    "JAK-STAT"
)

pi3k = get_row(
    "PI3K"
)


# ============================================================
# INTERPRETATION
# ============================================================

display(
    HTML(
        f"""
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        Two independent human single-cell cohorts show a
        <b>replicated disease-wide TGFβ/SMAD regulatory environment</b>
        in systemic sclerosis fibroblasts.

        <br><br>

        However, DPP4-positive fibroblasts are <b>not</b> the state with
        maximal canonical profibrotic signaling.

        Relative to DPP4-negative fibroblasts:

        <ul style="
            margin-top:7px;
            margin-bottom:7px;
        ">

          <li>
            TGFβ is lower:
            <b>{fmt_pair(tgfb)}</b>
          </li>

          <li>
            MAPK is lower:
            <b>{fmt_pair(mapk)}</b>
          </li>

          <li>
            NFκB is lower:
            <b>{fmt_pair(nfkb)}</b>
          </li>

          <li>
            JAK-STAT is lower:
            <b>{fmt_pair(jakstat)}</b>
          </li>

          <li>
            PI3K is higher:
            <b>{fmt_pair(pi3k)}</b>
          </li>

        </ul>

        <b>Interpretation:</b><br>

        The two independent cohorts replicate the same overall direction:
        DPP4 identifies a <b>distinct progenitor/ECM-associated fibroblast
        regulatory state</b>, rather than simply marking the fibroblast
        population with maximal canonical TGFβ/SMAD activity.

        <br><br>

        This is an <b>observational state comparison</b>.
        It does not contradict experimental studies showing that
        pharmacological or genetic perturbation of DPP4 can modulate
        profibrotic signaling.

        <br><br>

        <b>Verdict:</b><br>

        SSc-WIDE TGFβ/SMAD ACTIVATION —
        <b>STRONGLY SUPPORTED</b><br>

        DPP4+ = MAXIMAL CANONICAL TGFβ STATE —
        <b>CONTRADICTED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 9. Network medicine places DPP4 selectively near SSc fibrotic modules {display-mode: "form"}
# @markdown **Question:** Is DPP4 selectively positioned near fibrosis-relevant molecular modules in systemic sclerosis?
# @markdown
# @markdown **Data:** human SSc transcriptomic modules + curated fibroblast/ECM programs + STRING v12 interactome
# @markdown **Analysis:** degree-matched network proximity permutation + illustrative shortest paths
# @markdown **Analysis tools:** STRING v12 · NetworkX · degree-matched empirical null · Python
# @markdown **Primary network:** STRING functional network, confidence ≥ 700
# @markdown **Visualization:** Matplotlib
# @markdown
# @markdown **How to read:** more negative network-proximity z-scores indicate that a module lies closer to DPP4 than expected under the degree-matched null model. Statistical support is evaluated using FDR-adjusted **q < 0.05**.

import re
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Patch
from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# LOAD FROZEN DAVINCI RESULTS
# ============================================================

paths = load_tsv(
    "R4a_STRING_DPP4_shortest_paths.tsv"
)

network_summary = load_tsv(
    "R10_network_summary.tsv"
)

proximity_stats = load_tsv(
    "R10_proximity_statistics.tsv"
)


# ============================================================
# VALIDATED PRIMARY R10 RESULTS
#
# Used only as a last-resort fallback if column naming in the
# exported TSVs prevents automatic recovery.
#
# Primary network:
# STRING functional network, confidence >= 700
# 1000 degree-matched permutations
# ============================================================

# NOTE: hardcoded from the DaVinci R10 run. Any value filled from here is
# labelled "validated R10 primary fallback" in the printed `source` column.
R10_PRIMARY_FALLBACK = pd.DataFrame({

    "module_id": [
        "M1",
        "M2",
        "M3",
        "M4",
    ],

    "z": [
        -0.989,
        -1.711,
        -2.101,
        -4.520,
    ],

    "p": [
        0.179,
        0.02597,
        0.00999,
        0.000999,
    ],

    "q": [
        0.195,
        0.03896,
        0.01998,
        0.002398,
    ],
})


# ============================================================
# GENERAL COLUMN HELPERS
# ============================================================

def norm_col(x):
    """Normalize a column name for robust matching.

    Parameters
    ----------
    x : object
        Column name; converted to lower-case ``str``.

    Returns
    -------
    str
        The name with every non-alphanumeric character removed.
    """
    return re.sub(
        r"[^a-z0-9]+",
        "",
        str(x).lower()
    )


def numeric_candidate(df, column):
    """Check whether a column contains any usable numeric values.

    Parameters
    ----------
    df : pandas.DataFrame
        Table containing the column.
    column : str
        Column to test.

    Returns
    -------
    bool
        True if at least one value converts to a number.
    """
    try:
        x = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        return (
            x.notna().sum() > 0
        )

    except Exception:
        return False


def find_column(
    df,
    exact_candidates=None,
    contains_any=None,
    exclude_any=None,
    require_numeric=False,
):
    """Locate a column even when exported names vary.

    Exact matches (after :func:`norm_col` normalization) are tried first, then
    fuzzy substring matches.

    Parameters
    ----------
    df : pandas.DataFrame
        Table to search.
    exact_candidates : list of str, optional
        Names accepted as exact matches after normalization.
    contains_any : list of str, optional
        For the fuzzy pass, the normalized name must contain one of these.
    exclude_any : list of str, optional
        For the fuzzy pass, names containing any of these are skipped.
    require_numeric : bool, default False
        If True, only columns with usable numeric values are returned.

    Returns
    -------
    str or None
        The matching column name, or ``None`` if nothing matches.
    """

    exact_candidates = (
        exact_candidates
        or []
    )

    contains_any = (
        contains_any
        or []
    )

    exclude_any = (
        exclude_any
        or []
    )

    normalized = {
        col: norm_col(col)
        for col in df.columns
    }

    # --------------------------------------------------------
    # Exact normalized matches first
    # --------------------------------------------------------

    wanted = {
        norm_col(x)
        for x in exact_candidates
    }

    for col, ncol in normalized.items():

        if ncol in wanted:

            if (
                not require_numeric
                or
                numeric_candidate(
                    df,
                    col
                )
            ):
                return col

    # --------------------------------------------------------
    # Fuzzy matching second
    # --------------------------------------------------------

    for col, ncol in normalized.items():

        if exclude_any:

            if any(
                norm_col(x) in ncol
                for x in exclude_any
            ):
                continue

        if contains_any:

            if not any(
                norm_col(x) in ncol
                for x in contains_any
            ):
                continue

        if (
            require_numeric
            and
            not numeric_candidate(
                df,
                col
            )
        ):
            continue

        return col

    return None


# ============================================================
# PRIMARY NETWORK FILTER
# ============================================================

def filter_primary_network(df):
    """Keep only rows for the primary STRING network (functional, >= 700).

    Rows are first selected by text labels containing ``"functional"`` and
    ``"700"`` or ``"0.7"``; otherwise by a numeric confidence/threshold column
    equal to 700 or 0.7. If neither applies, the table is returned unchanged.

    Parameters
    ----------
    df : pandas.DataFrame
        R10 table that may contain several network configurations.

    Returns
    -------
    pandas.DataFrame
        Copy of the filtered (or unfiltered) table.
    """

    if len(df) == 0:
        return df.copy()

    x = df.copy()

    # --------------------------------------------------------
    # Search all text columns for explicit functional700 labels
    # --------------------------------------------------------

    text_cols = [
        c for c in x.columns
        if (
            x[c].dtype == object
            or
            str(x[c].dtype).startswith(
                "string"
            )
        )
    ]

    if text_cols:

        row_text = (
            x[text_cols]
            .fillna("")
            .astype(str)
            .agg(
                " ".join,
                axis=1
            )
            .str.lower()
        )

        primary_mask = (
            row_text.str.contains(
                "functional",
                regex=False
            )
            &
            (
                row_text.str.contains(
                    "700",
                    regex=False
                )
                |
                row_text.str.contains(
                    "0.7",
                    regex=False
                )
            )
        )

        if primary_mask.any():

            return (
                x[
                    primary_mask
                ]
                .copy()
            )

    # --------------------------------------------------------
    # Try numeric confidence/threshold column
    # --------------------------------------------------------

    confidence_col = find_column(
        x,

        exact_candidates=[
            "confidence",
            "confidence_cutoff",
            "score_cutoff",
            "string_score",
            "threshold",
            "min_score",
            "score_threshold",
        ],

        contains_any=[
            "confidence",
            "cutoff",
            "threshold",
        ],

        require_numeric=True,
    )

    if confidence_col is not None:

        vals = pd.to_numeric(
            x[
                confidence_col
            ],
            errors="coerce"
        )

        mask700 = (
            np.isclose(
                vals,
                700,
                equal_nan=False
            )
            |
            np.isclose(
                vals,
                0.7,
                equal_nan=False
            )
        )

        if mask700.any():

            x = (
                x[
                    mask700
                ]
                .copy()
            )

    return x


# ============================================================
# MODULE IDENTIFICATION
# ============================================================

def identify_module(value):
    """Map a module description or identifier to ``"M1"``-``"M4"``.

    Explicit ``M1``-``M4`` tokens are used first, then keyword rules:
    leading-edge/recurrent/ECM module -> M4, fibroblast -> M3,
    SSc up/upregulated -> M2, SSc significant/broad/all significant -> M1.

    Parameters
    ----------
    value : object
        Module label or ID; converted to ``str``.

    Returns
    -------
    str or None
        Module ID, or ``None`` if no rule matches.
    """

    text = str(
        value
    ).strip()

    upper = text.upper()

    # Explicit M1-M4
    match = re.search(
        r"\bM([1-4])\b",
        upper
    )

    if match:

        return (
            "M"
            +
            match.group(1)
        )

    lower = text.lower()

    # Semantic fallback
    if (
        "leading edge" in lower
        or
        "recurrent" in lower
        or
        (
            "ecm" in lower
            and
            "module" in lower
        )
    ):
        return "M4"

    if "fibroblast" in lower:
        return "M3"

    if (
        "ssc up" in lower
        or
        "upregulated" in lower
        or
        "up-regulated" in lower
    ):
        return "M2"

    if (
        "ssc significant" in lower
        or
        "broad" in lower
        or
        "all significant" in lower
    ):
        return "M1"

    return None


# ============================================================
# BENJAMINI-HOCHBERG
# ============================================================

def bh_adjust(pvalues):
    """Benjamini-Hochberg FDR correction without another library.

    Parameters
    ----------
    pvalues : array_like
        P-values; non-finite entries are ignored and returned as NaN.

    Returns
    -------
    numpy.ndarray
        BH-adjusted q-values, capped at 1, in the input order.
    """

    p = np.asarray(
        pvalues,
        dtype=float
    )

    q = np.full(
        p.shape,
        np.nan,
        dtype=float
    )

    valid = np.isfinite(
        p
    )

    if not valid.any():
        return q

    pv = p[
        valid
    ]

    m = len(
        pv
    )

    order = np.argsort(
        pv
    )

    ranked = pv[
        order
    ]

    adjusted = (
        ranked
        *
        m
        /
        np.arange(
            1,
            m + 1
        )
    )

    adjusted = np.minimum.accumulate(
        adjusted[::-1]
    )[::-1]

    adjusted = np.minimum(
        adjusted,
        1.0
    )

    restored = np.empty(
        m
    )

    restored[
        order
    ] = adjusted

    q[
        valid
    ] = restored

    return q


# ============================================================
# EXTRACT MODULE STATISTICS FROM ANY R10 TABLE
# ============================================================

def extract_stats_from_table(
    df,
    source_name,
):
    """Recover module, z-score, p-value and q-value from an R10 table.

    Works regardless of exact column naming by combining
    :func:`filter_primary_network`, :func:`find_column` and
    :func:`identify_module`.

    Parameters
    ----------
    df : pandas.DataFrame
        R10 proximity or summary table.
    source_name : str
        Label recorded in the ``source`` column of the output.

    Returns
    -------
    pandas.DataFrame
        One row per module with columns ``module_id``, ``source``, ``z``,
        ``p`` and ``q`` (NaN where not found); empty if no module column is
        found.
    """

    x = filter_primary_network(
        df
    )

    if len(x) == 0:

        return pd.DataFrame()


    # --------------------------------------------------------
    # Module column
    # --------------------------------------------------------

    module_col = find_column(
        x,

        exact_candidates=[
            "module",
            "module_id",
            "module_name",
            "gene_set",
            "geneset",
            "set_name",
            "target_module",
        ],

        contains_any=[
            "module",
            "geneset",
            "gene_set",
        ],
    )


    if module_col is None:

        # Search every text column for M1-M4
        for col in x.columns:

            vals = (
                x[col]
                .astype(str)
                .map(
                    identify_module
                )
            )

            if vals.notna().sum() >= 2:

                module_col = col
                break


    if module_col is None:

        return pd.DataFrame()


    x["module_id"] = (
        x[
            module_col
        ]
        .map(
            identify_module
        )
    )


    x = x[
        x[
            "module_id"
        ].isin(
            [
                "M1",
                "M2",
                "M3",
                "M4",
            ]
        )
    ].copy()


    if len(x) == 0:

        return pd.DataFrame()


    # --------------------------------------------------------
    # z-score
    # --------------------------------------------------------

    z_col = find_column(
        x,

        exact_candidates=[
            "z",
            "z_score",
            "zscore",
            "proximity_z",
            "network_proximity_z",
            "z_proximity",
        ],

        contains_any=[
            "zscore",
            "proximityz",
        ],

        require_numeric=True,
    )


    # broader z fallback
    if z_col is None:

        for col in x.columns:

            ncol = norm_col(
                col
            )

            if (
                "z" in ncol
                and
                numeric_candidate(
                    x,
                    col
                )
            ):

                vals = pd.to_numeric(
                    x[col],
                    errors="coerce"
                )

                # z-scores usually include negative values
                if (
                    vals.notna().sum() > 0
                    and
                    (
                        vals < 0
                    ).any()
                ):

                    z_col = col
                    break


    # --------------------------------------------------------
    # q / FDR
    # --------------------------------------------------------

    q_col = find_column(
        x,

        exact_candidates=[
            "q",
            "q_BH",
            "q_value",
            "qvalue",
            "FDR",
            "fdr_bh",
            "padj",
            "p_adj",
            "adjusted_p",
            "adjusted_p_value",
        ],

        contains_any=[
            "qvalue",
            "qbh",
            "fdr",
            "padj",
            "adjustedp",
        ],

        require_numeric=True,
    )


    # --------------------------------------------------------
    # empirical / raw p
    # --------------------------------------------------------

    p_col = find_column(
        x,

        exact_candidates=[
            "p",
            "p_value",
            "pvalue",
            "p_val",
            "pval",
            "p_empirical",
            "empirical_p",
            "empirical_p_value",
            "empirical_p_lower",
            "p_lower",
            "perm_p",
            "permutation_p",
        ],

        contains_any=[
            "empiricalp",
            "permutationp",
            "permp",
            "pvalue",
            "pval",
        ],

        exclude_any=[
            "adj",
            "fdr",
            "q",
        ],

        require_numeric=True,
    )


    # --------------------------------------------------------
    # Build compact output
    # --------------------------------------------------------

    out = pd.DataFrame({
        "module_id":
            x[
                "module_id"
            ]
            .astype(str),

        "source":
            source_name,
    })


    if z_col is not None:

        out["z"] = pd.to_numeric(
            x[
                z_col
            ],
            errors="coerce"
        )

    else:

        out["z"] = np.nan


    if p_col is not None:

        out["p"] = pd.to_numeric(
            x[
                p_col
            ],
            errors="coerce"
        )

    else:

        out["p"] = np.nan


    if q_col is not None:

        out["q"] = pd.to_numeric(
            x[
                q_col
            ],
            errors="coerce"
        )

    else:

        out["q"] = np.nan


    # Keep one row per module from each source
    out = (
        out
        .drop_duplicates(
            "module_id"
        )
        .reset_index(
            drop=True
        )
    )

    return out


# ============================================================
# RECOVER R10 STATISTICS
# ============================================================

candidate_tables = [

    (
        proximity_stats,
        "R10_proximity_statistics.tsv"
    ),

    (
        network_summary,
        "R10_network_summary.tsv"
    ),
]


extracted = []


for table, name in candidate_tables:

    tmp = extract_stats_from_table(
        table,
        name
    )

    if len(tmp) > 0:

        extracted.append(
            tmp
        )


# ============================================================
# START WITH MODULE FRAME
# ============================================================

prox = pd.DataFrame({

    "module_id": [
        "M1",
        "M2",
        "M3",
        "M4",
    ]
})


prox[
    "z"
] = np.nan

prox[
    "p"
] = np.nan

prox[
    "q"
] = np.nan

prox[
    "source"
] = ""


# ============================================================
# MERGE AUTOMATICALLY EXTRACTED VALUES
# ============================================================

for table in extracted:

    for _, row in table.iterrows():

        module = str(
            row[
                "module_id"
            ]
        )

        mask = (
            prox[
                "module_id"
            ]
            ==
            module
        )

        if not mask.any():
            continue


        for col in [
            "z",
            "p",
            "q",
        ]:

            value = row[
                col
            ]

            if (
                pd.notna(
                    value
                )
                and
                prox.loc[
                    mask,
                    col
                ].isna().all()
            ):

                prox.loc[
                    mask,
                    col
                ] = float(
                    value
                )


        if (
            row.get(
                "source",
                ""
            )
        ):

            old = prox.loc[
                mask,
                "source"
            ].iloc[0]

            src = str(
                row[
                    "source"
                ]
            )

            if old:

                if src not in old:

                    prox.loc[
                        mask,
                        "source"
                    ] = (
                        old
                        +
                        " + "
                        +
                        src
                    )

            else:

                prox.loc[
                    mask,
                    "source"
                ] = src


# ============================================================
# IF p EXISTS BUT q DOES NOT, CALCULATE BH
# ============================================================

if (
    prox[
        "p"
    ].notna().sum()
    >=
    2
):

    calculated_q = bh_adjust(
        prox[
            "p"
        ].values
    )

    for i in range(
        len(
            prox
        )
    ):

        if (
            pd.isna(
                prox.loc[
                    i,
                    "q"
                ]
            )
            and
            pd.notna(
                calculated_q[
                    i
                ]
            )
        ):

            prox.loc[
                i,
                "q"
            ] = calculated_q[
                i
            ]


# ============================================================
# FILL ONLY MISSING VALUES FROM VALIDATED PRIMARY R10 RESULTS
# ============================================================

fallback = (
    R10_PRIMARY_FALLBACK
    .set_index(
        "module_id"
    )
)


for i, row in prox.iterrows():

    module = row[
        "module_id"
    ]

    for col in [
        "z",
        "p",
        "q",
    ]:

        if pd.isna(
            prox.loc[
                i,
                col
            ]
        ):

            prox.loc[
                i,
                col
            ] = fallback.loc[
                module,
                col
            ]

            if (
                "validated R10 primary fallback"
                not in
                prox.loc[
                    i,
                    "source"
                ]
            ):

                if prox.loc[
                    i,
                    "source"
                ]:

                    prox.loc[
                        i,
                        "source"
                    ] += (
                        " + validated R10 primary fallback"
                    )

                else:

                    prox.loc[
                        i,
                        "source"
                    ] = (
                        "validated R10 primary fallback"
                    )


# ============================================================
# PRESENTATION LABELS
# ============================================================

MODULE_LABELS = {

    "M1":
        "Broad SSc gene set",

    "M2":
        "SSc-upregulated genes",

    "M3":
        "Fibroblast-state module",

    "M4":
        "ECM / fibrotic module",
}


MODULE_DETAILS = {

    "M1":
        "all significant disease genes",

    "M2":
        "genes increased in SSc skin",

    "M3":
        "fibroblast-centered program",

    "M4":
        "recurrent fibrosis / ECM program",
}


module_order = [
    "M1",
    "M2",
    "M3",
    "M4",
]


prox[
    "module_id"
] = pd.Categorical(
    prox[
        "module_id"
    ],

    categories=module_order,

    ordered=True,
)


prox = (
    prox
    .sort_values(
        "module_id"
    )
    .reset_index(
        drop=True
    )
)


prox[
    "label"
] = (
    prox[
        "module_id"
    ]
    .astype(str)
    .map(
        MODULE_LABELS
    )
)


prox[
    "detail"
] = (
    prox[
        "module_id"
    ]
    .astype(str)
    .map(
        MODULE_DETAILS
    )
)


prox[
    "significant"
] = (
    prox[
        "q"
    ]
    <
    0.05
)


# ============================================================
# PREPARE STRING PATH EXAMPLES
# ============================================================

p = paths.copy()


if "connected" in p.columns:

    p[
        "connected_bool"
    ] = (
        p[
            "connected"
        ]
        .astype(str)
        .str.lower()
        .isin(
            [
                "true",
                "1",
                "yes",
            ]
        )
    )

else:

    p[
        "connected_bool"
    ] = (
        pd.to_numeric(
            p[
                "n_hops"
            ],
            errors="coerce"
        )
        .notna()
    )


p[
    "n_hops"
] = pd.to_numeric(
    p[
        "n_hops"
    ],
    errors="coerce",
)


def get_path(gene):
    """Return the first connected STRING shortest path from DPP4 to a gene.

    Reads the module-level table ``p`` built in this cell.

    Parameters
    ----------
    gene : str
        Target gene symbol, e.g. ``"COL1A1"``.

    Returns
    -------
    dict
        Keys ``gene``, ``path`` (``"not connected"`` if absent) and ``hops``
        (NaN if absent).
    """

    x = p[
        (
            p[
                "target_gene"
            ]
            ==
            gene
        )
        &
        (
            p[
                "connected_bool"
            ]
        )
    ]


    if len(x) == 0:

        return {
            "gene":
                gene,

            "path":
                "not connected",

            "hops":
                np.nan,
        }


    row = x.iloc[0]


    return {

        "gene":
            gene,

        "path":
            str(
                row[
                    "path"
                ]
            ),

        "hops":
            float(
                row[
                    "n_hops"
                ]
            ),
    }


example_paths = [

    get_path(
        "THBS1"
    ),

    get_path(
        "COL1A1"
    ),

    get_path(
        "ACTA2"
    ),
]


# ============================================================
# COLORS
# ============================================================

SUPPORT = "#218C5A"
NOT_SIG = "#B7C0C8"

TEXT = "#172033"
MUTED = "#64748B"

GRID = "#E5E7EB"

CALLOUT_BG = "#F7F9FB"
CALLOUT_BORDER = "#D7DEE5"


# ============================================================
# FIGURE LAYOUT
# ============================================================

fig = plt.figure(
    figsize=(
        14.8,
        7.4
    ),

    dpi=180,

    facecolor="white",
)


gs = GridSpec(
    nrows=3,
    ncols=2,

    figure=fig,

    height_ratios=[
        0.15,
        0.70,
        0.15,
    ],

    width_ratios=[
        1.48,
        0.52,
    ],

    hspace=0.24,
    wspace=0.18,
)


ax_header = fig.add_subplot(
    gs[
        0,
        :
    ]
)

ax_main = fig.add_subplot(
    gs[
        1,
        0
    ]
)

ax_paths = fig.add_subplot(
    gs[
        1,
        1
    ]
)

ax_footer = fig.add_subplot(
    gs[
        2,
        :
    ]
)


ax_header.axis(
    "off"
)

ax_paths.axis(
    "off"
)

ax_footer.axis(
    "off"
)


# ============================================================
# HEADER
# ============================================================

ax_header.text(
    0.5,
    0.72,

    (
        "DPP4 shows selective network proximity "
        "to fibrosis-focused SSc modules"
    ),

    ha="center",
    va="center",

    fontsize=18,

    fontweight="bold",

    color=TEXT,
)


ax_header.text(
    0.5,
    0.25,

    (
        "The broad SSc gene set is not significantly proximal, "
        "whereas disease-upregulated, fibroblast and ECM modules are"
    ),

    ha="center",
    va="center",

    fontsize=11.2,

    color=MUTED,
)


# ============================================================
# MAIN RESULT
# ============================================================

y = np.arange(
    len(
        prox
    )
)


z_values = (
    prox[
        "z"
    ]
    .astype(float)
    .values
)


xmin = min(
    -5.25,

    float(
        np.nanmin(
            z_values
        )
    )
    -
    0.55
)


xmax = 0.72


ax_main.set_xlim(
    xmin,
    xmax,
)


# ============================================================
# LOLLIPOPS
# ============================================================

for i, row in prox.iterrows():

    z = float(
        row[
            "z"
        ]
    )

    q = float(
        row[
            "q"
        ]
    )

    significant = bool(
        row[
            "significant"
        ]
    )


    color = (
        SUPPORT
        if significant
        else
        NOT_SIG
    )


    # --------------------------------------------------------
    # Stem from module to zero
    # --------------------------------------------------------

    ax_main.hlines(
        y=i,

        xmin=z,
        xmax=0,

        color=color,

        linewidth=7,

        alpha=0.24,

        zorder=1,
    )


    # --------------------------------------------------------
    # Module estimate
    # --------------------------------------------------------

    ax_main.scatter(
        z,
        i,

        s=135,

        color=color,

        edgecolor="white",

        linewidth=1.5,

        zorder=3,
    )


    # --------------------------------------------------------
    # Statistics label
    # --------------------------------------------------------

    if q < 0.001:

        q_text = (
            "q < 0.001"
        )

    else:

        q_text = (
            f"q = {q:.3f}"
        )


    ax_main.text(
        z + 0.10,
        i,

        (
            f"z = {z:.2f}  ·  {q_text}"
        ),

        ha="left",
        va="center",

        fontsize=9.5,

        color=(
            SUPPORT
            if significant
            else
            MUTED
        ),

        fontweight=(
            "bold"
            if significant
            else
            "normal"
        ),

        zorder=4,
    )


# ============================================================
# Y LABELS
# ============================================================

ax_main.set_yticks(
    y
)


ax_main.set_yticklabels(
    [
        (
            f"{label}\n"
            f"{detail}"
        )

        for label, detail
        in zip(
            prox[
                "label"
            ],

            prox[
                "detail"
            ],
        )
    ],

    fontsize=10.3,
)


ax_main.invert_yaxis()


# ============================================================
# ZERO REFERENCE
# ============================================================

ax_main.axvline(
    0,

    linestyle="--",

    linewidth=1.1,

    color="#94A3B8",
)


ax_main.set_xlabel(
    "Network-proximity z-score",

    fontsize=10.5,

    labelpad=8,
)


ax_main.set_title(
    "Formal degree-matched proximity to DPP4",

    loc="left",

    fontsize=13,

    fontweight="bold",

    pad=18,

    color=TEXT,
)


ax_main.text(
    0.00,
    1.025,

    (
        "← stronger proximity to DPP4 "
        "than expected"
    ),

    transform=ax_main.transAxes,

    ha="left",
    va="bottom",

    fontsize=9.3,

    color=MUTED,
)


ax_main.grid(
    axis="x",

    color=GRID,

    linewidth=0.8,
)


ax_main.set_axisbelow(
    True
)


ax_main.spines[
    "top"
].set_visible(
    False
)

ax_main.spines[
    "right"
].set_visible(
    False
)

ax_main.spines[
    "left"
].set_visible(
    False
)


ax_main.tick_params(
    axis="y",

    length=0,

    pad=10,
)


# ============================================================
# LEGEND
# ============================================================

legend_handles = [

    Patch(
        facecolor=SUPPORT,

        label="q < 0.05",
    ),

    Patch(
        facecolor=NOT_SIG,

        label="not significant",
    ),
]


ax_main.legend(
    handles=legend_handles,

    loc="lower left",

    bbox_to_anchor=(
        0.0,
        -0.18
    ),

    ncol=2,

    frameon=False,

    fontsize=9.2,
)


# ============================================================
# SIDE CALLOUT
# ============================================================

box = FancyBboxPatch(
    (
        0.02,
        0.05
    ),

    0.95,
    0.90,

    boxstyle=(
        "round,pad=0.018,"
        "rounding_size=0.025"
    ),

    transform=ax_paths.transAxes,

    facecolor=CALLOUT_BG,

    edgecolor=CALLOUT_BORDER,

    linewidth=1.2,
)


ax_paths.add_patch(
    box
)


ax_paths.text(
    0.08,
    0.89,

    "Illustrative STRING paths",

    transform=ax_paths.transAxes,

    ha="left",
    va="top",

    fontsize=12.2,

    fontweight="bold",

    color=TEXT,
)


ax_paths.text(
    0.08,
    0.81,

    (
        "Examples showing how DPP4 is\n"
        "connected to fibrosis-related genes"
    ),

    transform=ax_paths.transAxes,

    ha="left",
    va="top",

    fontsize=9.0,

    color=MUTED,

    linespacing=1.3,
)


# ============================================================
# PATH EXAMPLES
# ============================================================

start_y = 0.66
dy = 0.19


for i, item in enumerate(
    example_paths
):

    yy = (
        start_y
        -
        i * dy
    )


    ax_paths.text(
        0.08,
        yy,

        item[
            "gene"
        ],

        transform=ax_paths.transAxes,

        ha="left",
        va="top",

        fontsize=10.5,

        fontweight="bold",

        color=SUPPORT,
    )


    pretty_path = (
        item[
            "path"
        ]
        .replace(
            "->",
            " → "
        )
    )


    pretty_path = "\n".join(
        textwrap.wrap(
            pretty_path,
            width=32,
        )
    )


    ax_paths.text(
        0.08,
        yy - 0.052,

        pretty_path,

        transform=ax_paths.transAxes,

        ha="left",
        va="top",

        fontsize=8.9,

        color=TEXT,

        linespacing=1.25,
    )


    if pd.notna(
        item[
            "hops"
        ]
    ):

        hop_text = (
            f"{int(item['hops'])} network hops"
        )

    else:

        hop_text = ""


    ax_paths.text(
        0.08,
        yy - 0.115,

        hop_text,

        transform=ax_paths.transAxes,

        ha="left",
        va="top",

        fontsize=8.2,

        color=MUTED,
    )


# ============================================================
# METHOD NOTE
# ============================================================

ax_paths.text(
    0.08,
    0.07,

    (
        "STRING functional network ≥ 700\n"
        "1,000 degree-matched permutations"
    ),

    transform=ax_paths.transAxes,

    ha="left",
    va="bottom",

    fontsize=8.3,

    color=MUTED,

    linespacing=1.35,
)


# ============================================================
# FOOTER
# ============================================================

ax_footer.text(
    0.5,
    0.68,

    (
        "Take-home: DPP4 is not generically proximal to SSc genes; "
        "its network proximity becomes significant in the "
        "fibroblast / ECM-focused component of the disease."
    ),

    ha="center",
    va="center",

    fontsize=11.2,

    fontweight="bold",

    color=TEXT,
)


ax_footer.text(
    0.5,
    0.26,

    (
        "Network proximity indicates topological / functional relatedness — "
        "not causal direction or direct physical interaction."
    ),

    ha="center",
    va="center",

    fontsize=9.6,

    color=MUTED,

    style="italic",
)


# ============================================================
# FINAL SPACING
# ============================================================

fig.subplots_adjust(
    left=0.20,

    right=0.98,

    top=0.97,

    bottom=0.05,
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_09_DPP4_selective_network_proximity.png"
)


fig.savefig(
    OUTPUT_FIGURE,

    dpi=300,

    bbox_inches="tight",

    facecolor="white",
)


plt.show()


# ============================================================
# RESULT HELPERS
# ============================================================

def module_row(
    module
):
    """Return the proximity-statistics row for one module.

    Reads the module-level table ``prox`` built in this cell.

    Parameters
    ----------
    module : str
        Module ID, ``"M1"``-``"M4"``.

    Returns
    -------
    pandas.Series or None
        Matching row, or ``None`` if absent.
    """

    x = prox[
        prox[
            "module_id"
        ].astype(str)
        ==
        module
    ]

    if len(x) == 0:
        return None

    return x.iloc[0]


def format_module(
    module
):
    """Format a module's z-score and q-value for the result text.

    Parameters
    ----------
    module : str
        Module ID, ``"M1"``-``"M4"``.

    Returns
    -------
    str
        ``"z=<z>, q=<q>"`` (``q<0.001`` when small), or ``"NA"``.
    """

    row = module_row(
        module
    )

    if row is None:
        return "NA"

    z = float(
        row[
            "z"
        ]
    )

    q = float(
        row[
            "q"
        ]
    )


    if q < 0.001:

        q_text = (
            "q<0.001"
        )

    else:

        q_text = (
            f"q={q:.3f}"
        )


    return (
        f"z={z:.2f}, {q_text}"
    )


# ============================================================
# RESULT
# ============================================================

display(
    HTML(
        f"""
        <div style="
            border-left:4px solid #218C5A;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.55;
        ">

        <b>Result</b><br>

        Degree-matched network analysis does <b>not</b> identify
        significant DPP4 proximity to the broad SSc gene set
        (<b>{format_module("M1")}</b>).

        <br><br>

        In contrast, DPP4 becomes significantly closer than expected
        when the analysis focuses on progressively more
        fibrosis-relevant molecular modules:

        <ul style="
            margin-top:7px;
            margin-bottom:7px;
        ">

          <li>
            <b>SSc-upregulated genes:</b>
            {format_module("M2")}
          </li>

          <li>
            <b>Fibroblast-state module:</b>
            {format_module("M3")}
          </li>

          <li>
            <b>ECM / fibrotic module:</b>
            {format_module("M4")}
          </li>

        </ul>

        <b>Interpretation:</b><br>

        DPP4 is not broadly embedded across all molecular features
        associated with systemic sclerosis. Instead, its network
        position is selectively closer to the
        <b>fibroblast- and ECM-centered component of the disease</b>.

        <br><br>

        The STRING paths shown beside the formal test are
        <b>illustrative examples</b> that make this network position
        biologically interpretable. They do not demonstrate a causal
        signaling cascade.

        <br><br>

        <b>Verdict:</b><br>

        SELECTIVE DPP4 PROXIMITY TO SSc FIBROTIC MODULES —
        <b>SUPPORTED</b>

        </div>
        """
    )
)


# ============================================================
# SMALL TRACEABILITY CHECK
# ============================================================

print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

print(
    "\nNetwork statistics used in the figure:"
)

display(
    prox[
        [
            "module_id",
            "label",
            "z",
            "p",
            "q",
            "source",
        ]
    ]
)

# @title 10. Human PK supports systemic target engagement and defines the dermal exposure requirement {display-mode: "form"}
# @markdown **Question:** Does clinically achievable human vildagliptin exposure provide a pharmacological basis for sustained DPP4 inhibition in skin?
# @markdown
# @markdown **Data:** published human vildagliptin PK/PD + biochemical DPP4 potency + R8 plasma/skin sensitivity model
# @markdown **Analysis:** human exposure-to-potency comparison + repeated-dose plasma PK simulation + skin-partition sensitivity analysis
# @markdown **Analysis tools:** Python · one-compartment oral PK model · repeated dosing · tissue equilibration model · PK/PD sensitivity analysis
# @markdown **Dose scenario:** 50 mg twice daily
# @markdown **Important:** the plasma model is anchored to published human PK; the skin component is a sensitivity analysis, not measured human dermal PK
# @markdown **Visualization:** DaVinci R5/R8 outputs + Matplotlib

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from PIL import Image
from IPython.display import display, HTML


# ============================================================
# LOAD FROZEN DAVINCI RESULTS
# ============================================================

thresholds = load_tsv(
    "R8_decision_threshold_summary.tsv"
)

plasma_diagnostic = load_tsv(
    "R8_plasma_model_diagnostic.tsv"
)


# ============================================================
# LOAD PRE-RENDERED DAVINCI FIGURES
# ============================================================

systemic_img = Image.open(
    data_file(
        "R5a_vildagliptin_exposure_vs_DPP4_IC50.png"
    )
).convert("RGB")


plasma_skin_img = Image.open(
    data_file(
        "R8_plasma_skin_concentration_profiles.png"
    )
).convert("RGB")


dermal_img = Image.open(
    data_file(
        "R8_dermal_DPP4_inhibition_profiles.png"
    )
).convert("RGB")


# ============================================================
# CROP WHITE MARGINS
# ============================================================

def crop_white_margin(
    image,
    threshold=248,
    padding=8,
):
    """Crop near-white margins from an RGB image.

    Parameters
    ----------
    image : PIL.Image.Image
        RGB image (a 3-channel array is assumed).
    threshold : int, default 248
        Pixels with any channel below this value count as content.
    padding : int, default 8
        Pixels of margin kept around the detected content.

    Returns
    -------
    PIL.Image.Image
        Cropped image, or the input unchanged if it is entirely near-white.
    """

    arr = np.asarray(image)

    mask = np.any(
        arr < threshold,
        axis=2,
    )

    coords = np.argwhere(mask)

    if coords.size == 0:
        return image

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)

    return image.crop(
        (
            max(0, x0 - padding),
            max(0, y0 - padding),
            min(image.width, x1 + padding),
            min(image.height, y1 + padding),
        )
    )


systemic_img = crop_white_margin(
    systemic_img
)

plasma_skin_img = crop_white_margin(
    plasma_skin_img
)

dermal_img = crop_white_margin(
    dermal_img
)


# ============================================================
# R8 THRESHOLD TABLE
# ============================================================

t = thresholds.copy()

t["IC50_nM"] = pd.to_numeric(
    t["IC50_nM"],
    errors="coerce"
)


for column in [
    "min_tested_Kpu_for_50pct_interval",
    "min_tested_Kpu_for_80pct_interval",
]:

    t[column] = pd.to_numeric(
        t[column],
        errors="coerce"
    )


def parse_target_percent(value):
    """Parse an inhibition target (e.g. 80% or 92%) from a table cell.

    A standalone ``80`` or ``92`` in the text is used first; otherwise the
    value is parsed as a number (``%`` removed) and fractions <= 1 are
    converted to percent.

    Parameters
    ----------
    value : object
        Cell value from the R8 ``target`` column.

    Returns
    -------
    float
        Target in percent, or NaN if it cannot be parsed.
    """

    text = str(value)

    match = re.search(
        r"(?<!\d)(80|92)(?!\d)",
        text
    )

    if match:
        return float(
            match.group(1)
        )

    try:

        value = float(
            text.replace("%", "")
        )

        if value <= 1:
            value *= 100

        return value

    except Exception:

        return np.nan


t["target_percent"] = (
    t["target"]
    .map(parse_target_percent)
)


# ============================================================
# EXTRACT CENTRAL R8 THRESHOLDS
# ============================================================

def threshold_value(
    ic50,
    target,
    column,
):
    """Look up one R8 skin-partition (Kpu) threshold.

    Reads the module-level table ``t`` built in this cell.

    Parameters
    ----------
    ic50 : float
        DPP4 IC50 scenario in nM.
    target : float
        Target inhibition in percent (80 or 92).
    column : str
        Threshold column to return.

    Returns
    -------
    float
        The threshold value.

    Raises
    ------
    RuntimeError
        If not exactly one row matches ``ic50`` and ``target``.
    """

    x = t[
        np.isclose(
            t["IC50_nM"],
            ic50
        )
        &
        np.isclose(
            t["target_percent"],
            target
        )
    ]

    if len(x) != 1:

        raise RuntimeError(
            f"Expected one threshold row for "
            f"IC50={ic50}, target={target}; "
            f"found {len(x)}."
        )

    return float(
        x.iloc[0][column]
    )


IC50_REFERENCE = 4.5


kpu_80_half = threshold_value(
    IC50_REFERENCE,
    80,
    "min_tested_Kpu_for_50pct_interval",
)

kpu_80_most = threshold_value(
    IC50_REFERENCE,
    80,
    "min_tested_Kpu_for_80pct_interval",
)

kpu_92_half = threshold_value(
    IC50_REFERENCE,
    92,
    "min_tested_Kpu_for_50pct_interval",
)

kpu_92_most = threshold_value(
    IC50_REFERENCE,
    92,
    "min_tested_Kpu_for_80pct_interval",
)


# ============================================================
# SANITY CHECK AGAINST FROZEN R8 RESULT
# ============================================================

expected = [
    (kpu_80_half, 0.10),
    (kpu_80_most, 0.20),
    (kpu_92_half, 0.20),
    (kpu_92_most, 0.50),
]


for observed, reference in expected:

    if not np.isclose(
        observed,
        reference
    ):

        raise RuntimeError(
            "R8 threshold mismatch: "
            f"observed={observed}, "
            f"expected={reference}"
        )


# ============================================================
# THREE-PANEL PHARMACOLOGY FIGURE
# ============================================================

fig = plt.figure(
    figsize=(15.0, 4.8),
    dpi=180,
)


gs = fig.add_gridspec(
    1,
    3,

    width_ratios=[
        0.85,
        1.08,
        1.07,
    ],

    left=0.025,
    right=0.985,

    top=0.76,
    bottom=0.08,

    wspace=0.10,
)


ax1 = fig.add_subplot(
    gs[0, 0]
)

ax2 = fig.add_subplot(
    gs[0, 1]
)

ax3 = fig.add_subplot(
    gs[0, 2]
)


# ============================================================
# PANEL A — HUMAN EXPOSURE VS POTENCY
# ============================================================

ax1.imshow(
    systemic_img,
    interpolation="lanczos"
)

ax1.axis("off")

ax1.set_title(
    "A. Human exposure vs DPP4 potency",
    fontsize=10.4,
    fontweight="bold",
    pad=6,
)


# ============================================================
# PANEL B — HUMAN-ANCHORED PLASMA SIMULATION
# ============================================================

ax2.imshow(
    plasma_skin_img,
    interpolation="lanczos"
)

ax2.axis("off")

ax2.set_title(
    "B. Repeated-dose plasma → skin simulation",
    fontsize=10.4,
    fontweight="bold",
    pad=6,
)


# ============================================================
# PANEL C — DERMAL PD
# ============================================================

ax3.imshow(
    dermal_img,
    interpolation="lanczos"
)

ax3.axis("off")

ax3.set_title(
    "C. Predicted dermal DPP4 inhibition",
    fontsize=10.4,
    fontweight="bold",
    pad=6,
)


# ============================================================
# GLOBAL TITLE
# ============================================================

fig.suptitle(
    "Human pharmacology supports systemic engagement; skin exposure remains the translational gate",
    fontsize=13.7,
    fontweight="bold",
    y=0.965,
)


fig.text(
    0.5,
    0.895,

    (
        "Published human PK anchors the plasma model, which is then "
        "propagated through hypothetical skin partition scenarios"
    ),

    ha="center",

    fontsize=9.3,
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_10_human_PK_dermal_translation.png"
)


fig.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight"
)


plt.show()


# ============================================================
# MODEL LOGIC — VISUAL SUMMARY
# ============================================================

display(
    HTML(
        """
        <div style="
            display:grid;
            grid-template-columns:1fr auto 1fr auto 1fr;
            align-items:center;
            gap:10px;
            margin:10px 0 12px 0;
        ">

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:10px 12px;
              text-align:center;
          ">
            <b>Published human PK</b><br>
            plasma Cmax / Tmax / exposure
          </div>

          <div style="
              font-size:22px;
              text-align:center;
          ">
            →
          </div>

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:10px 12px;
              text-align:center;
          ">
            <b>Repeated-dose plasma model</b><br>
            50 mg every 12 h
          </div>

          <div style="
              font-size:22px;
              text-align:center;
          ">
            →
          </div>

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:10px 12px;
              text-align:center;
          ">
            <b>Skin sensitivity model</b><br>
            Kpu → local concentration → DPP4 inhibition
          </div>

        </div>
        """
    )
)


# ============================================================
# COMPACT THRESHOLD TABLE
# ============================================================

decision_display = pd.DataFrame(
    {
        "Target inhibition": [
            "≥80%",
            "≥92%",
        ],

        "≥50% of dosing interval": [
            f"Kpu ≥ {kpu_80_half:.2f}",
            f"Kpu ≥ {kpu_92_half:.2f}",
        ],

        "≥80% of dosing interval": [
            f"Kpu ≥ {kpu_80_most:.2f}",
            f"Kpu ≥ {kpu_92_most:.2f}",
        ],
    }
)


display(
    HTML(
        """
        <div style="
            font-size:12px;
            font-weight:600;
            margin-top:5px;
            margin-bottom:5px;
        ">
        Central dermal sensitivity scenario — IC50 = 4.5 nM
        </div>
        """
    )
)


display(
    decision_display.style.hide(
        axis="index"
    )
)


# ============================================================
# OPTIONAL MODEL DIAGNOSTIC
#
# This is the frozen DaVinci diagnostic table.
# Keep collapsed/secondary in the notebook rather than
# rebuilding scientific calculations here.
# ============================================================

display(
    HTML(
        """
        <details style="
            margin-top:10px;
            margin-bottom:10px;
        ">
          <summary style="
              cursor:pointer;
              font-weight:600;
          ">
            Show R8 plasma-model diagnostic
          </summary>

          <div id="r8-diagnostic-placeholder"
               style="margin-top:8px;">
          </div>
        </details>
        """
    )
)

display(
    plasma_diagnostic
)


# ============================================================
# RESULT
# ============================================================

display(
    HTML(
        f"""
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        The R8 pharmacological model starts from
        <b>published human vildagliptin plasma pharmacokinetics</b>
        rather than from an arbitrary drug concentration.

        <br><br>

        A repeated-dose oral PK model was calibrated to the human
        plasma exposure scenario and used to generate the
        concentration-time profile that drives the subsequent
        skin-partition analysis.

        <br><br>

        This creates an explicit translational chain:

        <br><br>

        <b>
        clinical dose → human plasma exposure → hypothetical skin
        exposure → local DPP4 inhibition
        </b>

        <br><br>

        Under the central sensitivity scenario
        (<b>IC50 = {IC50_REFERENCE:.1f} nM</b>):

        <ul style="
            margin-top:7px;
            margin-bottom:7px;
        ">

          <li>
            ≥80% dermal inhibition for at least half of the dosing
            interval requires approximately
            <b>Kpu ≥ {kpu_80_half:.2f}</b>.
          </li>

          <li>
            ≥80% inhibition for most of the interval requires
            <b>Kpu ≥ {kpu_80_most:.2f}</b>.
          </li>

          <li>
            A stringent ≥92% inhibition target requires
            <b>Kpu ≥ {kpu_92_half:.2f}</b>
            for at least half of the interval and approximately
            <b>Kpu ≥ {kpu_92_most:.2f}</b>
            for most of the interval.
          </li>

        </ul>

        <b>Interpretation:</b><br>

        The plasma side of the model is anchored to
        <b>clinically achievable human exposure</b>.
        Therefore, systemic pharmacology is not the main uncertainty.

        The major translational unknown is the
        <b>free skin/plasma partition and actual dermal target
        engagement in patients with SSc</b>.

        <br><br>

        <b>Important:</b><br>

        This is <b>not a clinical skin PK study</b>.
        The plasma component is a simplified human-PK-anchored
        simulation, and the dermal component is a sensitivity model,
        not a validated skin PBPK model.

        <br><br>

        <b>Verdict:</b><br>

        HUMAN PLASMA PHARMACOLOGICAL ANCHOR —
        <b>SUPPORTED</b><br>

        SYSTEMIC DPP4 TARGET ENGAGEMENT —
        <b>SUPPORTED</b><br>

        DERMAL PHARMACOLOGICAL PLAUSIBILITY —
        <b>QUANTIFIED</b><br>

        HUMAN SSc SKIN TARGET ENGAGEMENT —
        <b>UNRESOLVED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 11. Functional studies provide a causal antifibrotic bridge from DPP4 to vildagliptin {display-mode: "form"}
# @markdown **Question:** Does experimental DPP4 inhibition reduce fibroblast activation and fibrosis, and is this effect observed with vildagliptin itself?
# @markdown
# @markdown **Evidence:** human dermal fibroblasts · genetic/pharmacological DPP4 perturbation · SSc-relevant fibrosis models · vildagliptin treatment
# @markdown **Key mechanistic anchor:** Soare et al. · PMID 31350829
# @markdown **Analysis:** curated functional and translational evidence synthesis
# @markdown **Analysis tools:** PubMed evidence curation · Python
# @markdown **Visualization:** mechanistic evidence bridge · Matplotlib

import matplotlib.pyplot as plt

from matplotlib.patches import (
    FancyBboxPatch,
    FancyArrowPatch,
)

from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# VALIDATE CURATED EVIDENCE TABLES
# ============================================================

preclinical = load_tsv(
    "R5b_preclinical_evidence_audit.tsv"
)

ladder = load_tsv(
    "R5b_translational_evidence_ladder.tsv"
)

# NOTE: `preclinical` and `ladder` are loaded (fail fast if missing) but not
# used below; the figure and verdict text in this cell are hardcoded.


# ============================================================
# PALETTE
# ============================================================

C = {
    "drug": "#E69F00",
    "target": "#2C7FB8",
    "cell": "#41AE76",
    "matrix": "#8064A2",
    "fibrosis": "#CB4B4B",

    "supported": "#2E8B57",
    "preclinical": "#2C7FB8",
    "replication": "#8064A2",
    "untested": "#9B684A",

    "text": "#17212B",
    "muted": "#64717D",
    "line": "#929CA6",

    "soft": "#F5F7F8",
    "border": "#C8D0D7",
}


# ============================================================
# FIGURE
#
# Compact layout:
#
# title
# ↓
# causal chain
# ↓
# evidence labels
# ↓
# key evidence cards
# ↓
# translational status
#
# ============================================================

fig, ax = plt.subplots(
    figsize=(14.4, 5.0),
    dpi=180,
)


fig.subplots_adjust(
    left=0.025,
    right=0.985,
    top=0.82,
    bottom=0.055,
)


ax.set_xlim(
    0,
    1,
)

ax.set_ylim(
    0,
    1,
)

ax.axis(
    "off"
)


# ============================================================
# GLOBAL TITLE
# ============================================================

fig.suptitle(
    (
        "Experimental perturbation supports "
        "an antifibrotic DPP4 mechanism"
    ),

    fontsize=16,
    fontweight="bold",

    y=0.965,
)


fig.text(
    0.5,
    0.915,

    (
        "Vildagliptin → DPP4 inhibition → "
        "fibroblast suppression → reduced fibrotic output"
    ),

    ha="center",
    va="center",

    fontsize=10.4,

    color=C["muted"],
)


# ============================================================
# HELPERS
# ============================================================

def draw_box(
    x,
    y,
    width,
    height,
    title,
    subtitle,
    color,
):
    """Draw a titled, centered rounded box on the module-level ``ax``.

    Parameters
    ----------
    x, y : float
        Box center in axes coordinates.
    width, height : float
        Box size in axes coordinates.
    title : str
        Bold title text.
    subtitle : str
        Smaller text under the title.
    color : str
        Border color.
    """

    box = FancyBboxPatch(
        (
            x - width / 2,
            y - height / 2,
        ),

        width,
        height,

        boxstyle=(
            "round,pad=0.012,"
            "rounding_size=0.018"
        ),

        facecolor="white",
        edgecolor=color,

        linewidth=2.0,

        zorder=3,
    )

    ax.add_patch(
        box
    )


    ax.text(
        x,
        y + 0.025,

        title,

        ha="center",
        va="center",

        fontsize=11.2,
        fontweight="bold",

        color=C["text"],

        zorder=4,
    )


    ax.text(
        x,
        y - 0.035,

        subtitle,

        ha="center",
        va="center",

        fontsize=8.5,

        color=C["muted"],

        linespacing=1.18,

        zorder=4,
    )


def draw_arrow(
    x1,
    x2,
    y,
):
    """Draw a horizontal arrow on the module-level ``ax``.

    Parameters
    ----------
    x1, x2 : float
        Start and end x positions in axes coordinates.
    y : float
        Vertical position in axes coordinates.
    """

    arrow = FancyArrowPatch(
        (
            x1,
            y,
        ),
        (
            x2,
            y,
        ),

        arrowstyle="-|>",

        mutation_scale=16,

        linewidth=1.8,

        color=C["line"],

        zorder=2,
    )

    ax.add_patch(
        arrow
    )


def draw_chip(
    x,
    y,
    text,
    color,
    width,
):
    """Draw a translucent label chip centered at ``(x, y)``.

    Parameters
    ----------
    x, y : float
        Chip center in axes coordinates.
    text : str
        Label text.
    color : str
        Chip and text color.
    width : float
        Chip width in axes coordinates.
    """

    chip = FancyBboxPatch(
        (
            x - width / 2,
            y - 0.027,
        ),

        width,
        0.054,

        boxstyle=(
            "round,pad=0.005,"
            "rounding_size=0.012"
        ),

        facecolor=color,
        edgecolor=color,

        linewidth=1.0,
        alpha=0.12,

        zorder=2,
    )

    ax.add_patch(
        chip
    )


    ax.text(
        x,
        y,

        text,

        ha="center",
        va="center",

        fontsize=8.2,
        fontweight="bold",

        color=color,

        zorder=3,
    )


def draw_info_card(
    x,
    y,
    width,
    height,
    heading,
    title,
    text,
    accent,
):
    """Draw an evidence card with heading, title and body text.

    Parameters
    ----------
    x, y : float
        Lower-left corner in axes coordinates.
    width, height : float
        Card size in axes coordinates.
    heading : str
        Small colored heading.
    title : str
        Bold title.
    text : str
        Body text along the bottom of the card.
    accent : str
        Border and heading color.
    """

    card = FancyBboxPatch(
        (
            x,
            y,
        ),

        width,
        height,

        boxstyle=(
            "round,pad=0.010,"
            "rounding_size=0.016"
        ),

        facecolor=C["soft"],
        edgecolor=accent,

        linewidth=1.25,
    )

    ax.add_patch(
        card
    )


    ax.text(
        x + 0.018,
        y + height - 0.027,

        heading,

        ha="left",
        va="top",

        fontsize=8.8,
        fontweight="bold",

        color=accent,
    )


    ax.text(
        x + 0.018,
        y + height - 0.060,

        title,

        ha="left",
        va="top",

        fontsize=10.1,
        fontweight="bold",

        color=C["text"],
    )


    ax.text(
        x + 0.018,
        y + 0.023,

        text,

        ha="left",
        va="bottom",

        fontsize=8.2,

        color=C["muted"],
    )


# ============================================================
# MAIN CAUSAL CHAIN
# ============================================================

centers = [
    0.10,
    0.30,
    0.50,
    0.70,
    0.90,
]


box_width = 0.165
box_height = 0.205

main_y = 0.675


draw_box(
    centers[0],
    main_y,
    box_width,
    box_height,

    "Vildagliptin",

    (
        "Approved DPP4 inhibitor\n"
        "clinically achievable exposure"
    ),

    C["drug"],
)


draw_box(
    centers[1],
    main_y,
    box_width,
    box_height,

    "DPP4 / CD26",

    (
        "Pharmacological +\n"
        "genetic perturbation"
    ),

    C["target"],
)


draw_box(
    centers[2],
    main_y,
    box_width,
    box_height,

    "Fibroblast activation",

    (
        "↓ activation markers\n"
        "↓ profibrotic phenotype"
    ),

    C["cell"],
)


draw_box(
    centers[3],
    main_y,
    box_width,
    box_height,

    "Collagen / ECM",

    (
        "↓ matrix-associated\n"
        "fibrotic output"
    ),

    C["matrix"],
)


draw_box(
    centers[4],
    main_y,
    box_width,
    box_height,

    "Tissue fibrosis",

    (
        "Reduced fibrosis in\n"
        "preclinical models"
    ),

    C["fibrosis"],
)


# ============================================================
# ARROWS
# ============================================================

for i in range(
    len(centers) - 1
):

    draw_arrow(
        centers[i]
        +
        box_width / 2
        +
        0.006,

        centers[i + 1]
        -
        box_width / 2
        -
        0.006,

        main_y,
    )


# ============================================================
# EVIDENCE TYPE CHIPS
# ============================================================

chip_y = 0.475


draw_chip(
    0.20,
    chip_y,

    "drug-specific evidence",

    C["drug"],

    0.155,
)


draw_chip(
    0.40,
    chip_y,

    "genetic + pharmacological",

    C["target"],

    0.175,
)


draw_chip(
    0.60,
    chip_y,

    "human dermal fibroblasts",

    C["cell"],

    0.170,
)


draw_chip(
    0.80,
    chip_y,

    "SSc-relevant in vivo models",

    C["fibrosis"],

    0.175,
)


# ============================================================
# KEY EVIDENCE CARDS
#
# Immediately below the causal chain.
# ============================================================

draw_info_card(
    x=0.055,
    y=0.245,

    width=0.54,
    height=0.135,

    heading=(
        "KEY DIRECT MECHANISTIC ANCHOR"
    ),

    title=(
        "Soare et al. · PMID 31350829"
    ),

    text=(
        "DPP4/CD26 perturbation reduces fibroblast activation "
        "and fibrosis in SSc-relevant experimental systems."
    ),

    accent=C["target"],
)


draw_info_card(
    x=0.625,
    y=0.245,

    width=0.32,
    height=0.135,

    heading=(
        "INDEPENDENT REPLICATION"
    ),

    title=(
        "Pulmonary fibrosis models"
    ),

    text=(
        "Vildagliptin also shows antifibrotic activity "
        "in an independent fibrotic organ context."
    ),

    accent=C["replication"],
)


# ============================================================
# TRANSLATIONAL STATUS
# ============================================================

ax.text(
    0.055,
    0.175,

    "Translational status",

    ha="left",
    va="center",

    fontsize=10.4,
    fontweight="bold",

    color=C["text"],
)


statuses = [
    {
        "x": 0.12,
        "label": "DPP4 causal biology",
        "status": "SUPPORTED",
        "color": C["supported"],
    },

    {
        "x": 0.38,
        "label": "Vildagliptin antifibrotic activity",
        "status": "PRECLINICAL",
        "color": C["preclinical"],
    },

    {
        "x": 0.67,
        "label": "Cross-organ replication",
        "status": "SUPPORTED",
        "color": C["replication"],
    },

    {
        "x": 0.89,
        "label": "Human SSc efficacy",
        "status": "UNTESTED",
        "color": C["untested"],
    },
]


for item in statuses:

    ax.scatter(
        item["x"],
        0.115,

        s=82,

        color=item[
            "color"
        ],

        zorder=3,
    )


    ax.text(
        item["x"],
        0.078,

        item["label"],

        ha="center",
        va="center",

        fontsize=8.2,

        color=C["text"],
    )


    ax.text(
        item["x"],
        0.045,

        item["status"],

        ha="center",
        va="center",

        fontsize=8.4,
        fontweight="bold",

        color=item[
            "color"
        ],
    )


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_11_functional_causal_bridge.png"
)


fig.savefig(
    OUTPUT_FIGURE,

    dpi=300,

    bbox_inches="tight",
)


plt.show()


# ============================================================
# RESULT
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        Experimental perturbation provides the causal link that
        observational human omics alone cannot establish.

        <br><br>

        Genetic and pharmacological inhibition of
        <b>DPP4/CD26</b> reduces fibroblast activation and
        fibrotic phenotypes, including evidence from
        <b>human dermal fibroblasts</b> and
        <b>SSc-relevant in vivo systems</b>.

        <br><br>

        Crucially, this evidence is not restricted to target biology:
        <b>vildagliptin itself shows antifibrotic activity
        preclinically</b>.

        <br><br>

        The strongest direct mechanistic anchor is
        <b>Soare et al. (PMID 31350829)</b>.
        Independent pulmonary-fibrosis experiments provide
        additional cross-organ support.

        <br><br>

        <b>Important:</b>
        these data support experimental plausibility,
        not therapeutic efficacy in patients with SSc.

        <br><br>

        <b>Verdict:</b><br>

        CAUSAL DPP4 ANTIFIBROTIC BIOLOGY —
        <b>SUPPORTED</b><br>

        VILDAGLIPTIN-SPECIFIC ANTIFIBROTIC ACTIVITY —
        <b>SUPPORTED PRECLINICALLY</b><br>

        HUMAN SSc EFFICACY —
        <b>UNTESTED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 12. Fibrotic fibroblast programs track clinical skin severity {display-mode: "form"}
# @markdown **Question:** Do the molecular fibroblast programs identified in SSc skin relate to clinical severity of cutaneous fibrosis?
# @markdown
# @markdown **Data:** GSE181549 longitudinal human SSc skin transcriptomics
# @markdown **Clinical endpoint:** modified Rodnan Skin Score (mRSS)
# @markdown **Analysis:** baseline donor-level program scores vs mRSS + adjusted clinical models
# @markdown **Analysis tools:** Python · Spearman correlation · multivariable regression
# @markdown **Visualization:** DaVinci clinical association output + Matplotlib clinical summary

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# LOAD REPRESENTATIVE DAVINCI FIGURE
# ============================================================

activated_img = Image.open(
    data_file(
        "R3c_activated_PRSS23_THBS1_vs_mRSS.png"
    )
).convert("RGB")


# ============================================================
# CROP WHITE MARGINS
# ============================================================

def crop_white_margin(
    image,
    threshold=248,
    padding=8,
):
    """Crop near-white margins from an RGB image.

    Parameters
    ----------
    image : PIL.Image.Image
        RGB image (a 3-channel array is assumed).
    threshold : int, default 248
        Pixels with any channel below this value count as content.
    padding : int, default 8
        Pixels of margin kept around the detected content.

    Returns
    -------
    PIL.Image.Image
        Cropped image, or the input unchanged if it is entirely near-white.
    """

    arr = np.asarray(
        image
    )

    mask = np.any(
        arr < threshold,
        axis=2,
    )

    coords = np.argwhere(
        mask
    )

    if coords.size == 0:
        return image

    y0, x0 = coords.min(
        axis=0
    )

    y1, x1 = coords.max(
        axis=0
    )

    x0 = max(
        0,
        x0 - padding
    )

    y0 = max(
        0,
        y0 - padding
    )

    x1 = min(
        image.width,
        x1 + padding
    )

    y1 = min(
        image.height,
        y1 + padding
    )

    return image.crop(
        (
            x0,
            y0,
            x1,
            y1,
        )
    )


activated_img = crop_white_margin(
    activated_img
)


# ============================================================
# FROZEN R3 CLINICAL RESULTS
#
# These are outputs of the completed DaVinci R3 analysis.
# No scientific statistics are recomputed in Colab.
# ============================================================

clinical = pd.DataFrame(
    [
        {
            "program": "Activated\nPRSS23 / THBS1",
            "rho": 0.704484,
            "adjusted_status": "SUPPORTED",
        },

        {
            "program": "Myofibroblast",
            "rho": 0.691531,
            "adjusted_status": "SUPPORTED",
        },

        {
            "program": "ECM",
            "rho": 0.551557,
            "adjusted_status": "SUPPORTED",
        },

        {
            "program": "Progenitor",
            "rho": 0.438975,
            "adjusted_status": "DIRECTIONAL",
        },

        {
            "program": "DPP4",
            "rho": -0.211494,
            "adjusted_status": "NOT SUPPORTED",
        },
    ]
)


# ============================================================
# COMPACT FIGURE
# ============================================================

fig = plt.figure(
    figsize=(12.8, 4.8),
    dpi=180,
)


gs = fig.add_gridspec(
    1,
    2,

    width_ratios=[
        1.05,
        0.95,
    ],

    left=0.045,
    right=0.98,

    top=0.77,
    bottom=0.14,

    wspace=0.27,
)


ax1 = fig.add_subplot(
    gs[0, 0]
)

ax2 = fig.add_subplot(
    gs[0, 1]
)


# ============================================================
# PANEL A — REPRESENTATIVE PATIENT-LEVEL ASSOCIATION
# ============================================================

ax1.imshow(
    activated_img,
    interpolation="lanczos",
)

ax1.axis(
    "off"
)

ax1.set_title(
    "A. Activated fibroblast program vs mRSS",
    fontsize=10.8,
    fontweight="bold",
    pad=6,
)


# ============================================================
# PANEL B — CLINICAL ASSOCIATION SUMMARY
# ============================================================

clinical_plot = (
    clinical
    .sort_values(
        "rho",
        ascending=True
    )
    .reset_index(
        drop=True
    )
)


y = np.arange(
    len(
        clinical_plot
    )
)


# Stems
for i, row in clinical_plot.iterrows():

    ax2.hlines(
        y=i,
        xmin=min(
            0,
            row[
                "rho"
            ]
        ),
        xmax=max(
            0,
            row[
                "rho"
            ]
        ),

        linewidth=1.5,
        alpha=0.35,
    )


# Plot supported / directional / unsupported separately
for status, marker, alpha in [
    (
        "SUPPORTED",
        "o",
        1.0,
    ),

    (
        "DIRECTIONAL",
        "o",
        0.55,
    ),

    (
        "NOT SUPPORTED",
        "X",
        1.0,
    ),
]:

    sub = clinical_plot[
        clinical_plot[
            "adjusted_status"
        ]
        ==
        status
    ]

    ax2.scatter(
        sub[
            "rho"
        ],
        sub.index,

        s=70,

        marker=marker,

        alpha=alpha,

        label=status,

        zorder=3,
    )


# Zero line
ax2.axvline(
    0,
    linestyle="--",
    linewidth=0.9,
    alpha=0.6,
)


# ============================================================
# LABEL VALUES
# ============================================================

for i, row in clinical_plot.iterrows():

    rho = row[
        "rho"
    ]

    offset = (
        0.035
        if rho >= 0
        else
        -0.035
    )

    ax2.text(
        rho + offset,
        i,

        f"{rho:.2f}",

        ha=(
            "left"
            if rho >= 0
            else
            "right"
        ),

        va="center",

        fontsize=8.8,

        fontweight="bold",
    )


ax2.set_yticks(
    y
)

ax2.set_yticklabels(
    clinical_plot[
        "program"
    ],
    fontsize=9.2,
)


ax2.set_xlabel(
    "Spearman correlation with baseline mRSS",
    fontsize=9.6,
    labelpad=6,
)


ax2.set_xlim(
    -0.40,
    0.82,
)


ax2.set_title(
    "B. Clinical relevance across fibroblast programs",
    fontsize=10.8,
    fontweight="bold",
    pad=6,
)


ax2.grid(
    axis="x",
    alpha=0.15,
)


ax2.set_axisbelow(
    True
)


ax2.spines[
    "top"
].set_visible(
    False
)

ax2.spines[
    "right"
].set_visible(
    False
)


ax2.legend(
    frameon=False,
    fontsize=8.0,
    loc="lower right",
)


# ============================================================
# GLOBAL TITLE
# ============================================================

fig.suptitle(
    "Fibrotic fibroblast programs track clinical skin severity",
    fontsize=13.8,
    fontweight="bold",
    y=0.965,
)


fig.text(
    0.5,
    0.895,

    (
        "Downstream activated, myofibroblast and ECM programs "
        "track mRSS more strongly than DPP4 expression itself"
    ),

    ha="center",
    fontsize=9.3,
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_12_fibroblast_programs_mRSS.png"
)


fig.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight",
)


plt.show()


# ============================================================
# RESULT
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        Molecular fibroblast programs identified in human SSc skin
        show clear relationships with the clinical severity of
        cutaneous fibrosis.

        <br><br>

        The strongest baseline associations with mRSS are:

        <ul style="
            margin-top:7px;
            margin-bottom:7px;
        ">

          <li>
            Activated PRSS23/THBS1:
            <b>ρ ≈ 0.70</b>
          </li>

          <li>
            Myofibroblast:
            <b>ρ ≈ 0.69</b>
          </li>

          <li>
            ECM:
            <b>ρ ≈ 0.55</b>
          </li>

        </ul>

        These downstream fibrotic programs also remain supported in
        adjusted clinical models.

        <br><br>

        <b>DPP4 behaves differently:</b>
        baseline DPP4 expression shows a weak negative association
        with mRSS (<b>ρ ≈ −0.21</b>) and is not supported as an
        independent positive severity biomarker.

        <br><br>

        <b>Interpretation:</b><br>

        DPP4 appears more useful as a
        <b>marker/participant of a disease-relevant fibroblast context</b>
        than as a direct quantitative biomarker of fibrosis severity.

        The clinically relevant endpoint lies downstream:
        <b>activated fibroblast → myofibroblast → ECM output</b>.

        <br><br>

        <b>Verdict:</b><br>

        FIBROTIC FIBROBLAST PROGRAMS ↔ mRSS —
        <b>SUPPORTED</b><br>

        DPP4 AS A POSITIVE SSc SEVERITY BIOMARKER —
        <b>NOT SUPPORTED</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 13. The opportunity is translational rather than biologically novel {display-mode: "form"}
# @markdown **Question:** Is vildagliptin for systemic sclerosis a new biological hypothesis, or an unresolved translational opportunity?
# @markdown
# @markdown **Sources:** PubMed · ClinicalTrials.gov · Cortellis review
# @markdown **Analysis:** structured precedent and development-gap audit
# @markdown **Analysis tools:** literature curation · ClinicalTrials.gov queries · Cortellis intelligence review · Python
# @markdown **Interpretation:** absence claims are restricted to the records reviewed

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
from IPython.display import display, HTML

# ============================================================
# LOAD CURATED RESULTS
# ============================================================

pubmed = load_tsv(
    "R6b_PubMed_evidence_class_summary.tsv"
)

ct_skin = load_tsv(
    "R6a_ClinicalTrials_skin_dermal_fibrosis.tsv"
)

ct_scleroderma = load_tsv(
    "R6a_ClinicalTrials_localized_scleroderma.tsv"
)

# NOTE: these three tables are loaded but not used below; the figure and
# verdict text in this cell are hardcoded.

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(13.5, 4.8),
    dpi=180
)

fig.subplots_adjust(
    left=0.035,
    right=0.98,
    top=0.80,
    bottom=0.08
)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ============================================================
# COLORS
# ============================================================

C = {
    "known": "#2C7FB8",
    "preclinical": "#41AE76",
    "gap": "#E69F00",
    "clinical": "#CB4B4B",
    "text": "#17212B",
    "muted": "#66727D",
    "line": "#949DA6",
    "soft": "#F5F7F8",
}

# ============================================================
# TITLE
# ============================================================

fig.suptitle(
    "The innovation is closing a translational gap",
    fontsize=15,
    fontweight="bold",
    y=0.96
)

fig.text(
    0.5,
    0.90,
    (
        "Antifibrotic DPP4 biology already has preclinical precedent; "
        "clinical development in SSc remains unresolved"
    ),
    ha="center",
    fontsize=10
)

# ============================================================
# HELPERS
# ============================================================

def box(x, title, subtitle, color, status):
    """Draw one stage of the translational continuum.

    The box has a fixed size and vertical position (y = 0.57).

    Parameters
    ----------
    x : float
        Box center x position in axes coordinates.
    title : str
        Bold title.
    subtitle : str
        Description under the title.
    color : str
        Border and status color.
    status : str
        Status label drawn at the bottom of the box.
    """

    w = 0.195
    h = 0.28
    y = 0.57

    p = FancyBboxPatch(
        (x - w/2, y - h/2),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor="white",
        edgecolor=color,
        linewidth=2
    )

    ax.add_patch(p)

    ax.text(
        x,
        y + 0.065,
        title,
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color=C["text"]
    )

    ax.text(
        x,
        y - 0.005,
        subtitle,
        ha="center",
        va="center",
        fontsize=8.7,
        color=C["muted"],
        linespacing=1.25
    )

    ax.text(
        x,
        y - 0.105,
        status,
        ha="center",
        fontsize=9,
        fontweight="bold",
        color=color
    )


def arrow(x1, x2):
    """Draw a horizontal arrow at y = 0.57 between continuum boxes.

    Parameters
    ----------
    x1, x2 : float
        Start and end x positions in axes coordinates.
    """

    ax.add_patch(
        FancyArrowPatch(
            (x1, 0.57),
            (x2, 0.57),
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=1.7,
            color=C["line"]
        )
    )

# ============================================================
# TRANSLATIONAL CONTINUUM
# ============================================================

centers = [
    0.12,
    0.37,
    0.62,
    0.87,
]

box(
    centers[0],
    "DPP4 antifibrotic biology",
    (
        "Fibroblast activation and\n"
        "fibrosis mechanisms reported"
    ),
    C["known"],
    "ESTABLISHED PRECEDENT"
)

box(
    centers[1],
    "Vildagliptin preclinical evidence",
    (
        "Drug-specific antifibrotic\n"
        "activity already reported"
    ),
    C["preclinical"],
    "PRECLINICAL SUPPORT"
)

box(
    centers[2],
    "Human SSc development",
    (
        "No interventional clinical\n"
        "development identified in\n"
        "the reviewed records"
    ),
    C["gap"],
    "TRANSLATIONAL GAP"
)

box(
    centers[3],
    "Human efficacy",
    (
        "Effect on skin fibrosis or\n"
        "mRSS remains untested"
    ),
    C["clinical"],
    "UNRESOLVED"
)

for i in range(3):
    arrow(
        centers[i] + 0.105,
        centers[i + 1] - 0.105
    )

# ============================================================
# NOVELTY MESSAGE
# ============================================================

ax.text(
    0.50,
    0.22,
    (
        "Innovation ≠ discovering that DPP4 can influence fibrosis"
    ),
    ha="center",
    fontsize=10.5,
    fontweight="bold",
    color=C["text"]
)

ax.text(
    0.50,
    0.15,
    (
        "Innovation = translating an approved DPP4 inhibitor into a "
        "human SSc fibroblast-state framework with explicit PK/PD and "
        "proof-of-mechanism criteria"
    ),
    ha="center",
    fontsize=9.3,
    color=C["muted"]
)

# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/Figure_13_translational_gap.png"
)

fig.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# RESULT
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        The antifibrotic biology of DPP4 is <b>not biologically novel</b>.
        Direct preclinical work already links DPP4 inhibition — including
        vildagliptin — to reduced fibroblast activation and fibrosis.

        <br><br>

        However, across the reviewed <b>PubMed, ClinicalTrials.gov and
        Cortellis records</b>, we did not identify human interventional
        development of vildagliptin for systemic sclerosis.

        <br><br>

        <b>Therefore, the opportunity is translational:</b><br>
        move an approved, systemically target-engaging drug from
        preclinical antifibrotic precedent into a
        <b>human SSc fibroblast-state and dermal proof-of-mechanism framework</b>.

        <br><br>

        <b>Important:</b>
        this should not be phrased as a universal claim that no patent,
        program or prior attempt exists. The conclusion applies to the
        <b>records reviewed</b>.

        <br><br>

        <b>Verdict:</b><br>

        BIOLOGICAL NOVELTY —
        <b>LOW</b><br>

        CLINICAL SSc REPURPOSING GAP —
        <b>SUPPORTED</b><br>

        TRANSLATIONAL OPPORTUNITY —
        <b>SUPPORTED</b>

        </div>
        """
    )
)

print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 14. Independent stress tests define the limits of the hypothesis {display-mode: "form"}
# @markdown **Question:** Do perturbational transcriptomics or human genetics independently strengthen the DPP4–SSc repurposing hypothesis?
# @markdown
# @markdown **R16:** vildagliptin + DPP4 genetic perturbation signatures from LINCS/L1000
# @markdown **R17:** GWAS Catalog · GTEx · Open Targets · Ensembl
# @markdown **Analysis:** human-disease signature reversal + GWAS/locus/eQTL audit
# @markdown **Analysis tools:** SigCom LINCS · Spearman reversal · Wilcoxon · BH-FDR · GWAS Catalog · GTEx · Open Targets
# @markdown **Primary R16 analysis:** top 500 up + 500 down disease genes · 24 h · 1.11 µM
# @markdown **Interpretation:** absence of additional support is treated as a stress test, not automatic falsification
# @markdown **Visualization:** Matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import FancyBboxPatch
from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# LOAD FROZEN DAVINCI RESULTS
# ============================================================

r16_all = load_tsv(
    "R16_primary_vildagliptin_summary.tsv"
)

r16_verdict = load_tsv(
    "R16_primary_vildagliptin_verdict.tsv"
)

r16_target = load_tsv(
    "R16_target_validation_verdict.tsv"
)

r16_concordance = load_tsv(
    "R16_drug_target_concordance.tsv"
)

r17 = load_tsv(
    "R17_human_genetics_summary.tsv"
)

# NOTE: only `r16_all` feeds the figure. The R16 verdict/target/concordance
# tables are loaded but unused, and `r17` is only checked for one row; the
# genetics cards and verdict text below are hardcoded.


# ============================================================
# NUMERIC CONVERSION
# ============================================================

numeric_cols = [
    "top_n_each_direction",
    "n_cell_lines",
    "median_rho",
    "CI95_median_low",
    "CI95_median_high",
    "fraction_reversal",
    "p_Wilcoxon_less_zero",
    "q_BH",
]

for col in numeric_cols:

    if col in r16_all.columns:

        r16_all[col] = pd.to_numeric(
            r16_all[col],
            errors="coerce"
        )


# ============================================================
# IMPORTANT — PRIMARY R16 ANALYSIS ONLY
#
# Frozen primary design:
# top 500 disease-up + top 500 disease-down genes.
#
# The table also contains top250/top1000 sensitivity analyses.
# Those must NOT be mixed into the primary visualization.
# ============================================================

if "top_n_each_direction" in r16_all.columns:

    r16 = r16_all[
        r16_all["top_n_each_direction"] == 500
    ].copy()

else:

    # Fallback only if the summary table is already primary-only.
    r16 = r16_all.copy()


# Integrity: exactly one row for R1, R11 and R2.
expected_datasets = {
    "R1",
    "R11",
    "R2",
}

observed_datasets = set(
    r16["dataset"]
    .astype(str)
)


if (
    len(r16) != 3
    or
    observed_datasets != expected_datasets
):

    raise RuntimeError(
        "Primary R16 filtering did not return exactly "
        "one result for R1, R11 and R2.\n"
        f"Rows found: {len(r16)}\n"
        f"Datasets: {sorted(observed_datasets)}\n"
        f"Available columns: {list(r16_all.columns)}"
    )


# ============================================================
# R16 ORDER / LABELS
# ============================================================

dataset_order = [
    "R1",
    "R11",
    "R2",
]

dataset_labels = {
    "R1": "GSE58095\nwhole skin",
    "R11": "GSE249279\nfibroblasts",
    "R2": "GSE138669\nfibroblasts",
}


r16["dataset"] = pd.Categorical(
    r16["dataset"],
    categories=dataset_order,
    ordered=True
)

r16 = (
    r16
    .sort_values("dataset")
    .reset_index(drop=True)
)

r16["display"] = (
    r16["dataset"]
    .astype(str)
    .map(dataset_labels)
)


# ============================================================
# R17 SUMMARY
# ============================================================

if len(r17) != 1:

    raise RuntimeError(
        f"Expected one R17 summary row; found {len(r17)}."
    )

g = r17.iloc[0]


genetics = [
    {
        "title": "Direct SSc GWAS",
        "subtitle": "association mapped to DPP4",
        "status": "NOT IDENTIFIED",
    },
    {
        "title": "DPP4 locus",
        "subtitle": "SSc association within ±500 kb",
        "status": "NOT IDENTIFIED",
    },
    {
        "title": "Relevant-tissue cis-eQTL",
        "subtitle": "skin / transformed fibroblasts",
        "status": "NOT IDENTIFIED",
    },
    {
        "title": "Colocalization",
        "subtitle": "pre-specified prerequisites met",
        "status": "NO CANDIDATE",
    },
]


# ============================================================
# COLORS
# ============================================================

C = {
    "R1": "#3572B8",
    "R11": "#7851A9",
    "R2": "#D97732",

    "zero": "#89939D",

    "negative": "#B85450",
    "negative_soft": "#FCF5F4",

    "text": "#18212B",
    "muted": "#66727D",

    "border": "#CDD3D9",
    "soft": "#F6F8FA",
}


# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(
    figsize=(12.8, 4.7),
    dpi=180
)


gs = fig.add_gridspec(
    1,
    2,

    width_ratios=[
        1.05,
        0.95,
    ],

    left=0.075,
    right=0.975,

    top=0.74,
    bottom=0.18,

    wspace=0.30,
)


ax1 = fig.add_subplot(
    gs[0, 0]
)

ax2 = fig.add_subplot(
    gs[0, 1]
)


# ============================================================
# PANEL A — PRIMARY VILDAGLIPTIN REVERSAL
# ============================================================

y = np.arange(
    len(r16)
)[::-1]


for i, row in r16.iterrows():

    yi = y[i]

    dataset = str(
        row["dataset"]
    )

    median = float(
        row["median_rho"]
    )

    ci_low = float(
        row["CI95_median_low"]
    )

    ci_high = float(
        row["CI95_median_high"]
    )

    ax1.errorbar(
        median,
        yi,

        xerr=np.array(
            [
                [median - ci_low],
                [ci_high - median],
            ]
        ),

        fmt="o",

        markersize=7.2,

        linewidth=1.7,

        capsize=0,

        color=C[dataset],

        zorder=3,
    )


    # q-value positioned consistently
    ax1.text(
        0.050,
        yi,

        f"q = {row['q_BH']:.2f}",

        ha="right",
        va="center",

        fontsize=8.3,

        color=C["muted"],
    )


# No reversal / mimicry boundary
ax1.axvline(
    0,

    linestyle="--",

    linewidth=1.0,

    color=C["zero"],

    alpha=0.8,
)


ax1.set_xlim(
    -0.052,
    0.052,
)

ax1.set_ylim(
    -0.60,
    2.60,
)


ax1.set_yticks(
    y
)

ax1.set_yticklabels(
    r16["display"],
    fontsize=9.0,
)


ax1.set_xlabel(
    "Median Spearman ρ: SSc disease effect vs perturbation",
    fontsize=9.2,
    labelpad=7,
)


ax1.tick_params(
    axis="x",
    labelsize=8.3,
)


ax1.grid(
    axis="x",
    alpha=0.15,
)

ax1.set_axisbelow(True)

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)


ax1.set_title(
    "A. Vildagliptin transcriptomic reversal",
    fontsize=10.8,
    fontweight="bold",
    pad=7,
)


# Direction labels inside the panel
ax1.text(
    0.02,
    0.97,

    "← reversal",

    transform=ax1.transAxes,

    ha="left",
    va="top",

    fontsize=8.3,

    color=C["muted"],
)


ax1.text(
    0.98,
    0.97,

    "mimicry →",

    transform=ax1.transAxes,

    ha="right",
    va="top",

    fontsize=8.3,

    color=C["muted"],
)


# ============================================================
# PANEL B — HUMAN GENETICS
# ============================================================

ax2.set_xlim(
    0,
    1
)

ax2.set_ylim(
    0,
    1
)

ax2.axis(
    "off"
)


ax2.set_title(
    "B. Direct human genetic support",
    fontsize=10.8,
    fontweight="bold",
    pad=7,
)


card_positions = [
    0.80,
    0.60,
    0.40,
    0.20,
]


for item, cy in zip(
    genetics,
    card_positions,
):

    card = FancyBboxPatch(
        (
            0.04,
            cy - 0.067,
        ),

        0.92,
        0.134,

        boxstyle=(
            "round,pad=0.010,"
            "rounding_size=0.015"
        ),

        facecolor=C["soft"],
        edgecolor=C["border"],

        linewidth=1.0,
    )

    ax2.add_patch(
        card
    )


    # Negative/not-identified icon
    ax2.scatter(
        0.105,
        cy,

        s=62,

        marker="X",

        color=C["negative"],

        zorder=3,
    )


    ax2.text(
        0.165,
        cy + 0.022,

        item["title"],

        ha="left",
        va="center",

        fontsize=9.2,
        fontweight="bold",

        color=C["text"],
    )


    ax2.text(
        0.165,
        cy - 0.025,

        item["subtitle"],

        ha="left",
        va="center",

        fontsize=8.1,

        color=C["muted"],
    )


    ax2.text(
        0.92,
        cy,

        item["status"],

        ha="right",
        va="center",

        fontsize=8.3,
        fontweight="bold",

        color=C["negative"],
    )


# ============================================================
# GLOBAL TITLE
# ============================================================

fig.suptitle(
    "Independent stress tests define the limits of the hypothesis",
    fontsize=13.8,
    fontweight="bold",
    y=0.965,
)


fig.text(
    0.5,
    0.895,

    (
        "Neither global LINCS reversal nor direct human genetics "
        "adds independent positive support"
    ),

    ha="center",

    fontsize=9.3,

    color=C["muted"],
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path(
    "/content/"
    "Figure_14_stress_tests_R16_R17.png"
)


fig.savefig(
    OUTPUT_FIGURE,

    dpi=300,

    bbox_inches="tight",
)


plt.show()


# ============================================================
# PRIMARY R16 VALUES
# ============================================================

r16_display = r16[
    [
        "dataset",
        "n_cell_lines",
        "median_rho",
        "CI95_median_low",
        "CI95_median_high",
        "q_BH",
    ]
].copy()


r16_display.columns = [
    "Dataset",
    "LINCS cell lines",
    "Median rho",
    "CI low",
    "CI high",
    "FDR q",
]


display(
    HTML(
        "<b>Primary R16 result — top 500 up + 500 down</b>"
    )
)

display(
    r16_display.style
    .format(
        {
            "Median rho": "{:.4f}",
            "CI low": "{:.4f}",
            "CI high": "{:.4f}",
            "FDR q": "{:.3f}",
        }
    )
    .hide(axis="index")
)


# ============================================================
# COMPACT STATUS STRIP
# ============================================================

display(
    HTML(
        """
        <div style="
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:10px;
            margin:12px 0;
        ">

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:9px 12px;
          ">
            <b>Vildagliptin / LINCS</b><br>
            <span style="
                color:#a34d47;
                font-weight:700;
            ">
            NOT REPLICATED
            </span>
          </div>

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:9px 12px;
          ">
            <b>DPP4 KO / KD</b><br>
            <span style="
                color:#a34d47;
                font-weight:700;
            ">
            NOT REPLICATED
            </span>
          </div>

          <div style="
              border:1px solid #ddd;
              border-radius:8px;
              padding:9px 12px;
          ">
            <b>Human genetics</b><br>
            <span style="
                color:#a34d47;
                font-weight:700;
            ">
            NOT IDENTIFIED
            </span>
          </div>

        </div>
        """
    )
)


# ============================================================
# INTERPRETATION
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:8px;
            line-height:1.52;
        ">

        <b>Result</b><br>

        The pre-specified primary LINCS analysis does
        <b>not demonstrate reproducible vildagliptin reversal</b>
        of human SSc disease signatures.

        The three independent human signatures show median
        correlations close to zero, with confidence intervals
        spanning zero and non-significant FDR values.

        <br><br>

        DPP4 CRISPR knockout and shRNA perturbations also fail to
        reproducibly reverse the same disease signatures.

        <br><br>

        Human genetics independently provides
        <b>no direct positive support</b>:
        no reviewed SSc GWAS association maps directly to DPP4,
        no association lies within the pre-specified ±500 kb locus,
        and no significant DPP4 cis-eQTL was identified in the
        reviewed skin/fibroblast GTEx contexts.

        <br><br>

        <b>Interpretation:</b><br>

        These results weaken claims of
        <b>global transcriptomic rescue</b> or
        <b>germline genetically driven DPP4 causality</b>.

        They do not directly falsify the pharmacological hypothesis.

        LINCS predominantly represents transformed cell-line
        perturbations rather than primary SSc dermal fibroblasts,
        while pharmacological modification of an acquired fibrotic
        state does not require DPP4 to be a germline disease-risk locus.

        <br><br>

        <b>Verdict:</b><br>

        VILDAGLIPTIN GLOBAL TRANSCRIPTOMIC REVERSAL —
        <b>NOT REPLICATED</b><br>

        DPP4 GENETIC-PERTURBATION REVERSAL —
        <b>NOT REPLICATED</b><br>

        DIRECT HUMAN GENETIC SUPPORT —
        <b>NOT IDENTIFIED</b><br>

        HYPOTHESIS FALSIFIED —
        <b>NO</b>

        </div>
        """
    )
)


print(
    f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}"
)

# @title 15. A disease-relevant proof-of-mechanism experiment is the decisive next step {display-mode: "form"}
# @markdown **Question:** What experiment would most directly determine whether vildagliptin should advance for cutaneous SSc?
# @markdown
# @markdown **Design:** primary human SSc dermal fibroblasts · TGFβ1 challenge · exposure-informed vildagliptin · DPP4 knockdown · antifibrotic readouts
# @markdown **Logic:** distinguish pharmacological failure from target/mechanistic failure
# @markdown **Primary endpoints:** DPP4 activity · PRSS23/THBS1 · ACTA2/TAGLN · collagen/ECM · matrix contraction
# @markdown **Analysis basis:** integrated human omics · pharmacology · functional literature · stress tests
# @markdown **Visualization:** translational go/no-go experiment · Matplotlib

import textwrap
import matplotlib.pyplot as plt

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# PALETTE
# ============================================================

C = {
    "sample": "#3572B8",
    "challenge": "#8064A2",
    "intervention": "#E69F00",
    "measurement": "#3C91A3",

    "go": "#2E8B57",
    "drug_fail": "#D97732",
    "target_fail": "#B85450",

    "text": "#1E2732",
    "muted": "#6B7682",
    "line": "#98A2AD",

    "soft": "#F6F8FA",
    "soft2": "#EEF2F5",
    "border": "#C9D1D9",
}


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(14.8, 7.0), dpi=180)
fig.subplots_adjust(left=0.025, right=0.985, top=0.83, bottom=0.05)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


# ============================================================
# TITLES
# ============================================================

fig.suptitle(
    "The decisive next step is a human SSc proof-of-mechanism experiment",
    fontsize=16,
    fontweight="bold",
    y=0.965,
)

fig.text(
    0.5,
    0.918,
    (
        "Test whether exposure-relevant vildagliptin engages DPP4 "
        "and suppresses fibrotic activity in primary dermal fibroblasts"
    ),
    ha="center",
    fontsize=10,
    color=C["muted"],
)


# ============================================================
# HELPERS
# ============================================================

def wrap_text(text, width):
    """Wrap text to a fixed line width.

    Parameters
    ----------
    text : str
        Text to wrap.
    width : int
        Maximum characters per line.

    Returns
    -------
    str
        Text with newline-separated lines.
    """
    return "\n".join(textwrap.wrap(text, width=width))


def rounded_box(
    x,
    y,
    w,
    h,
    title,
    subtitle,
    edge,
    fill="white",
    title_size=10.2,
    subtitle_size=8.3,
    subtitle_width=28,
):
    """Draw a rounded box with a title and wrapped subtitle.

    Parameters
    ----------
    x, y : float
        Lower-left corner in axes coordinates.
    w, h : float
        Box size in axes coordinates.
    title : str
        Bold title.
    subtitle : str
        Description, wrapped to ``subtitle_width`` characters.
    edge : str
        Border color.
    fill : str, default "white"
        Fill color.
    title_size, subtitle_size : float
        Font sizes.
    subtitle_width : int, default 28
        Wrap width for the subtitle.
    """
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor=fill,
        edgecolor=edge,
        linewidth=1.7,
    )
    ax.add_patch(patch)

    ax.text(
        x + w / 2,
        y + h * 0.63,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        fontweight="bold",
        color=C["text"],
    )

    ax.text(
        x + w / 2,
        y + h * 0.29,
        wrap_text(subtitle, subtitle_width),
        ha="center",
        va="center",
        fontsize=subtitle_size,
        color=C["muted"],
        linespacing=1.15,
    )


def small_chip(
    x,
    y,
    w,
    h,
    text,
    edge=C["border"],
):
    """Draw a small labeled chip (text wrapped at 14 characters).

    Parameters
    ----------
    x, y : float
        Lower-left corner in axes coordinates.
    w, h : float
        Chip size in axes coordinates.
    text : str
        Label text.
    edge : str, default ``C["border"]``
        Border color.
    """
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.004,rounding_size=0.009",
        facecolor=C["soft"],
        edgecolor=edge,
        linewidth=1.0,
    )
    ax.add_patch(patch)

    ax.text(
        x + w / 2,
        y + h / 2,
        wrap_text(text, 14),
        ha="center",
        va="center",
        fontsize=7.7,
        color=C["text"],
        linespacing=1.08,
    )


def horizontal_arrow(x1, x2, y):
    """Draw a horizontal arrow on the module-level ``ax``.

    Parameters
    ----------
    x1, x2 : float
        Start and end x positions in axes coordinates.
    y : float
        Vertical position in axes coordinates.
    """
    ax.add_patch(
        FancyArrowPatch(
            (x1, y),
            (x2, y),
            arrowstyle="-|>",
            mutation_scale=15,
            linewidth=1.5,
            color=C["line"],
        )
    )


def decision_box(
    x,
    y,
    w,
    h,
    heading,
    rule,
    color,
):
    """Draw a go/no-go decision box with a heading and wrapped rule.

    Parameters
    ----------
    x, y : float
        Lower-left corner in axes coordinates.
    w, h : float
        Box size in axes coordinates.
    heading : str
        Bold colored heading.
    rule : str
        Decision rule, wrapped at 43 characters.
    color : str
        Border and heading color.
    """
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.015",
        facecolor="white",
        edgecolor=color,
        linewidth=1.5,
    )
    ax.add_patch(patch)

    ax.text(
        x + 0.016,
        y + h - 0.022,
        heading,
        ha="left",
        va="top",
        fontsize=10.0,
        fontweight="bold",
        color=color,
    )

    ax.text(
        x + 0.016,
        y + h - 0.052,
        wrap_text(rule, 43),
        ha="left",
        va="top",
        fontsize=8.2,
        color=C["text"],
        linespacing=1.18,
    )


# ============================================================
# SECTION 1 — EXPERIMENTAL DESIGN
# ============================================================

ax.text(
    0.04,
    0.79,
    "1  Experimental design",
    fontsize=11.6,
    fontweight="bold",
    color=C["text"],
)

x_positions = [0.045, 0.285, 0.525, 0.765]
box_w = 0.19
box_h = 0.125
box_y = 0.585

rounded_box(
    x_positions[0],
    box_y,
    box_w,
    box_h,
    "Primary dermal fibroblasts",
    "SSc lesional samples + healthy donor controls",
    C["sample"],
    title_size=10.0,
    subtitle_size=8.2,
    subtitle_width=26,
)

rounded_box(
    x_positions[1],
    box_y,
    box_w,
    box_h,
    "Fibrotic challenge",
    "± TGFβ1 stimulation to induce fibrotic activity",
    C["challenge"],
    title_size=10.0,
    subtitle_size=8.2,
    subtitle_width=26,
)

rounded_box(
    x_positions[2],
    box_y,
    box_w,
    box_h,
    "Experimental arms",
    "vehicle · vildagliptin · DPP4 KD · KD + drug · nintedanib",
    C["intervention"],
    title_size=10.0,
    subtitle_size=8.0,
    subtitle_width=28,
)

rounded_box(
    x_positions[3],
    box_y,
    box_w,
    box_h,
    "Mechanistic response",
    "target engagement + antifibrotic phenotype",
    C["measurement"],
    title_size=10.0,
    subtitle_size=8.2,
    subtitle_width=24,
)

horizontal_arrow(x_positions[0] + box_w, x_positions[1] - 0.008, box_y + box_h / 2)
horizontal_arrow(x_positions[1] + box_w, x_positions[2] - 0.008, box_y + box_h / 2)
horizontal_arrow(x_positions[2] + box_w, x_positions[3] - 0.008, box_y + box_h / 2)


# ============================================================
# EXPERIMENTAL ARM CHIPS
# ============================================================

arm_y = 0.485
chip_h = 0.045
chip_w = 0.088
chip_gap = 0.010
arm_start = 0.525

ax.text(
    0.62,
    0.545,
    "Experimental comparison arms",
    ha="center",
    fontsize=8.6,
    fontweight="bold",
    color=C["muted"],
)

arms = [
    "Vehicle",
    "Vildagliptin\nPK-informed",
    "DPP4\nknockdown",
    "KD +\nvildagliptin",
    "Nintedanib\npositive control",
]

for i, label in enumerate(arms):
    small_chip(
        arm_start + i * (chip_w + chip_gap),
        arm_y,
        chip_w,
        chip_h,
        label,
    )


# ============================================================
# SECTION 2 — PRE-SPECIFIED MEASUREMENTS
# ============================================================

ax.text(
    0.04,
    0.435,
    "2  Pre-specified measurements",
    fontsize=11.6,
    fontweight="bold",
    color=C["text"],
)

measure_y = 0.315
measure_w = 0.165
measure_h = 0.078
measure_x = [0.045, 0.235, 0.425, 0.615, 0.805]

measurements = [
    ("Target engagement", "DPP4 enzymatic activity", C["sample"]),
    ("Activated fibroblast", "PRSS23 · THBS1", C["challenge"]),
    ("Myofibroblast", "ACTA2 · TAGLN", C["intervention"]),
    ("ECM production", "COL1A1 · soluble collagen", C["measurement"]),
    ("Functional output", "matrix contraction", C["go"]),
]

for x, (title, subtitle, color) in zip(measure_x, measurements):
    rounded_box(
        x,
        measure_y,
        measure_w,
        measure_h,
        title,
        subtitle,
        color,
        title_size=9.0,
        subtitle_size=7.8,
        subtitle_width=22,
    )

ax.text(
    0.5,
    0.275,
    "Target engagement should be confirmed before interpreting the antifibrotic phenotype",
    ha="center",
    fontsize=8.5,
    color=C["muted"],
    style="italic",
)


# ============================================================
# SECTION 3 — DECISION LOGIC
# ============================================================

ax.text(
    0.04,
    0.215,
    "3  Decision logic",
    fontsize=11.6,
    fontweight="bold",
    color=C["text"],
)

decision_y = 0.045
decision_h = 0.145
decision_w = 0.29

decision_box(
    0.045,
    decision_y,
    decision_w,
    decision_h,
    "GO — drug and mechanism supported",
    (
        "Vildagliptin reduces DPP4 activity and suppresses fibroblast "
        "activation, collagen/ECM output and matrix contraction at "
        "exposure-relevant concentrations."
    ),
    C["go"],
)

decision_box(
    0.357,
    decision_y,
    decision_w,
    decision_h,
    "DRUG FAILURE — target may remain valid",
    (
        "DPP4 knockdown suppresses the fibrotic phenotype, but "
        "exposure-relevant vildagliptin does not. The target remains "
        "plausible, but this repurposing fails."
    ),
    C["drug_fail"],
)

decision_box(
    0.669,
    decision_y,
    decision_w,
    decision_h,
    "TARGET / MECHANISM FAILURE",
    (
        "Neither DPP4 knockdown nor pharmacological inhibition produces "
        "a meaningful antifibrotic phenotype despite adequate "
        "experimental target assessment."
    ),
    C["target_fail"],
)


# ============================================================
# EXPORT
# ============================================================

OUTPUT_FIGURE = Path("/content/Figure_15_decisive_proof_of_mechanism.png")

fig.savefig(
    OUTPUT_FIGURE,
    dpi=300,
    bbox_inches="tight",
)

plt.show()


# ============================================================
# INTERPRETATION
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:13px 17px;
            margin-top:10px;
            line-height:1.52;
        ">

        <b>Why this experiment?</b><br>

        The current evidence supports a disease-relevant human fibroblast context,
        experimental antifibrotic DPP4 biology and clinically achievable systemic
        pharmacology.

        <br><br>

        The decisive unresolved question is whether
        <b>vildagliptin itself can engage DPP4 and suppress fibrotic activity
        in primary human SSc dermal fibroblasts at pharmacologically relevant exposure</b>.

        <br><br>

        <b>Interpretation logic:</b>

        <ul style="margin-top:7px; margin-bottom:7px;">
          <li><b>GO:</b> vildagliptin engages DPP4 and suppresses the fibrotic phenotype.</li>
          <li><b>Drug failure:</b> DPP4 knockdown works, but vildagliptin does not.</li>
          <li><b>Target/mechanism failure:</b> DPP4 perturbation itself fails to suppress fibrosis.</li>
        </ul>

        <b>Primary go/no-go measurements:</b><br>
        DPP4 activity · PRSS23/THBS1 · ACTA2/TAGLN · COL1A1/soluble collagen · matrix contraction

        <br><br>

        <b>Verdict:</b><br>
        DECISIVE NEXT STEP — <b>DISEASE-RELEVANT HUMAN PROOF-OF-MECHANISM</b>

        </div>
        """
    )
)

print(f"\nHigh-resolution figure saved to:\n{OUTPUT_FIGURE}")

# @title 16. Integrated evidence and final translational decision {display-mode: "form"}
# @markdown **Decision question:** Does the complete evidence package justify advancing vildagliptin for cutaneous systemic sclerosis?
# @markdown
# @markdown **Evidence integration:** human transcriptomics · independent single-cell replication · fibroblast-state biology · network medicine · human PK/PD · functional perturbation · clinical relevance · translational precedent
# @markdown **Stress tests:** LINCS perturbational transcriptomics · human genetics
# @markdown **Decision level:** disease-relevant proof-of-mechanism — **not clinical efficacy**
# @markdown **Visualization:** interactive evidence landscape · Plotly

import pandas as pd
import plotly.graph_objects as go

from pathlib import Path
from IPython.display import display, HTML


# ============================================================
# FINAL EVIDENCE LANDSCAPE
#
# x-position indicates the ROLE of each result in the decision.
# It is NOT a quantitative score or ranking.
# ============================================================

evidence = [

    # ========================================================
    # SUPPORTING HUMAN EVIDENCE
    # ========================================================

    {
        "domain": "Human disease",
        "evidence": "Human SSc fibrotic program",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "Human SSc skin shows strong collagen and ECM remodeling.",
        "basis":
            "GSE58095 · differential expression · Reactome/GSEA",
    },

    {
        "domain": "Human disease",
        "evidence": "DPP4 cellular localization",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "DPP4 localizes to a fibroblast-relevant cellular compartment.",
        "basis":
            "GSE138669 · human skin scRNA-seq",
    },

    {
        "domain": "Human disease",
        "evidence": "Independent scRNA replication",
        "decision_role": "Supports hypothesis",
        "status": "STRONGLY SUPPORTED",
        "finding":
            "DPP4 associations with progenitor and ECM fibroblast programs replicate independently.",
        "basis":
            "GSE138669 + GSE249279",
    },

    {
        "domain": "Human disease",
        "evidence": "Fibrotic programs ↔ mRSS",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "Activated, myofibroblast and ECM programs strongly track clinical skin severity.",
        "basis":
            "GSE181549 · donor-level mRSS analysis",
    },


    # ========================================================
    # TARGET / MECHANISM
    # ========================================================

    {
        "domain": "Target & mechanism",
        "evidence": "Branch-aware fibroblast organization",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "DPP4-high, activated and ECM-associated organization shares a fibroblast branch.",
        "basis":
            "PAGA · pseudotime · donor-level occupancy",
    },

    {
        "domain": "Target & mechanism",
        "evidence": "Network proximity",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "DPP4 lies closer than expected to multiple SSc fibrotic modules.",
        "basis":
            "STRING v12 · degree-matched empirical null",
    },

    {
        "domain": "Target & mechanism",
        "evidence": "Functional DPP4 perturbation",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "Genetic and pharmacological DPP4 inhibition reduces fibroblast activation and fibrosis.",
        "basis":
            "Human dermal fibroblasts + SSc-relevant experimental models",
    },

    {
        "domain": "Target & mechanism",
        "evidence": "SSc TGFβ/SMAD environment",
        "decision_role": "Supports hypothesis",
        "status": "STRONGLY SUPPORTED",
        "finding":
            "Canonical TGFβ/SMAD activity is reproducibly increased in SSc fibroblasts.",
        "basis":
            "PROGENy · CollecTRI · two independent human cohorts",
    },


    # ========================================================
    # DRUG / PHARMACOLOGY
    # ========================================================

    {
        "domain": "Drug & pharmacology",
        "evidence": "Vildagliptin antifibrotic activity",
        "decision_role": "Supports hypothesis",
        "status": "PRECLINICAL",
        "finding":
            "Vildagliptin itself reduces fibrotic phenotypes in preclinical models.",
        "basis":
            "Functional literature · Soare et al. + independent studies",
    },

    {
        "domain": "Drug & pharmacology",
        "evidence": "Human systemic DPP4 engagement",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED",
        "finding":
            "Clinically achievable human exposure strongly supports systemic DPP4 inhibition.",
        "basis":
            "Published human PK/PD · exposure-to-potency analysis",
    },

    {
        "domain": "Drug & pharmacology",
        "evidence": "Human-anchored plasma simulation",
        "decision_role": "Supports hypothesis",
        "status": "QUANTIFIED",
        "finding":
            "Repeated-dose plasma exposure was modeled from clinically anchored human PK.",
        "basis":
            "50 mg twice daily · repeated-dose PK simulation",
    },

    {
        "domain": "Drug & pharmacology",
        "evidence": "Dermal exposure requirement",
        "decision_role": "Supports hypothesis",
        "status": "QUANTIFIED",
        "finding":
            "Skin/plasma exposure required for sustained dermal DPP4 inhibition was quantified.",
        "basis":
            "R8 dermal PK/PD sensitivity analysis",
    },


    # ========================================================
    # TRANSLATIONAL OPPORTUNITY
    # ========================================================

    {
        "domain": "Translation",
        "evidence": "Clinical development gap",
        "decision_role": "Supports hypothesis",
        "status": "SUPPORTED GAP",
        "finding":
            "Human SSc development was not identified among the reviewed records.",
        "basis":
            "PubMed · ClinicalTrials.gov · Cortellis",
    },


    # ========================================================
    # MODEL REFINEMENTS
    # ========================================================

    {
        "domain": "Model refinement",
        "evidence": "Global DPP4 expression",
        "decision_role": "Refines model",
        "status": "NOT GLOBALLY INCREASED",
        "finding":
            "DPP4 is not globally increased in SSc skin.",
        "basis":
            "GSE58095 + GSE138669 + GSE249279",
    },

    {
        "domain": "Model refinement",
        "evidence": "DPP4 as severity biomarker",
        "decision_role": "Refines model",
        "status": "NOT SUPPORTED",
        "finding":
            "DPP4 itself does not behave as a positive mRSS severity biomarker.",
        "basis":
            "GSE181549",
    },

    {
        "domain": "Model refinement",
        "evidence": "Single linear trajectory",
        "decision_role": "Refines model",
        "status": "NOT SUPPORTED",
        "finding":
            "A universal DPP4 → activated → myofibroblast → ECM trajectory is not supported.",
        "basis":
            "Pseudotime + PAGA",
    },

    {
        "domain": "Model refinement",
        "evidence": "DPP4+ canonical signaling state",
        "decision_role": "Refines model",
        "status": "DISTINCT STATE",
        "finding":
            "DPP4-positive fibroblasts are not the state with maximal TGFβ/MAPK/NFκB activity.",
        "basis":
            "PROGENy + CollecTRI · R2 + R11",
    },


    # ========================================================
    # STRESS TESTS
    # ========================================================

    {
        "domain": "Stress test",
        "evidence": "Vildagliptin LINCS reversal",
        "decision_role": "No additional support",
        "status": "NOT REPLICATED",
        "finding":
            "Vildagliptin did not reproducibly reverse three human SSc transcriptomic signatures.",
        "basis":
            "LINCS/L1000 · primary 24 h, 1.11 µM analysis",
    },

    {
        "domain": "Stress test",
        "evidence": "DPP4 KO/KD LINCS reversal",
        "decision_role": "No additional support",
        "status": "NOT REPLICATED",
        "finding":
            "DPP4 genetic perturbation also failed to reproducibly reverse SSc signatures.",
        "basis":
            "LINCS CRISPR + shRNA",
    },

    {
        "domain": "Stress test",
        "evidence": "Human genetics",
        "decision_role": "No additional support",
        "status": "NOT IDENTIFIED",
        "finding":
            "Direct DPP4–SSc GWAS/locus/relevant-tissue eQTL support was not identified.",
        "basis":
            "GWAS Catalog · GTEx · Open Targets",
    },


    # ========================================================
    # EXPERIMENTAL GATE
    # ========================================================

    {
        "domain": "Experimental gate",
        "evidence": "Human dermal PK/PD",
        "decision_role": "Requires experiment",
        "status": "DIRECTLY TESTABLE",
        "finding":
            "Actual vildagliptin exposure and DPP4 inhibition in human SSc skin remain unmeasured.",
        "basis":
            "Paired plasma/skin PK + dermal DPP4 activity",
    },

    {
        "domain": "Experimental gate",
        "evidence": "Human SSc efficacy",
        "decision_role": "Requires experiment",
        "status": "UNTESTED",
        "finding":
            "Therapeutic effect on skin fibrosis or mRSS has not been established.",
        "basis":
            "Clinical testing only after successful proof-of-mechanism",
    },
]


df = pd.DataFrame(evidence)


# ============================================================
# DECISION AXIS
#
# Categorical only — NOT an evidence-strength scale.
# ============================================================

ROLE_ORDER = [
    "Supports hypothesis",
    "Refines model",
    "No additional support",
    "Requires experiment",
]

ROLE_X = {
    role: i
    for i, role in enumerate(ROLE_ORDER)
}


df["x"] = (
    df["decision_role"]
    .map(ROLE_X)
)


# ============================================================
# ROW ORDER
# ============================================================

DOMAIN_ORDER = [
    "Human disease",
    "Target & mechanism",
    "Drug & pharmacology",
    "Translation",
    "Model refinement",
    "Stress test",
    "Experimental gate",
]


df["domain"] = pd.Categorical(
    df["domain"],
    categories=DOMAIN_ORDER,
    ordered=True,
)


df = (
    df
    .sort_values(
        [
            "domain",
            "evidence",
        ],
        ascending=[
            True,
            True,
        ],
    )
    .reset_index(
        drop=True
    )
)


# Reverse so first item appears at top
df["y"] = (
    len(df)
    -
    1
    -
    df.index
)


# ============================================================
# DOMAIN COLORS
#
# Color = independent evidence domain
# Position = decision role
# ============================================================

DOMAIN_COLORS = {

    "Human disease":
        "#3572B8",

    "Target & mechanism":
        "#2E8B57",

    "Drug & pharmacology":
        "#E69F00",

    "Translation":
        "#8064A2",

    "Model refinement":
        "#D28A2D",

    "Stress test":
        "#B85450",

    "Experimental gate":
        "#9B684A",
}


# ============================================================
# FIGURE
# ============================================================

fig = go.Figure()


for domain in DOMAIN_ORDER:

    sub = df[
        df["domain"] == domain
    ]

    if len(sub) == 0:
        continue

    fig.add_trace(
        go.Scatter(

            x=sub["x"],

            y=sub["y"],

            mode="markers",

            name=domain,

            marker=dict(
                size=15,
                color=DOMAIN_COLORS[
                    domain
                ],
                line=dict(
                    color="white",
                    width=1.2,
                ),
            ),

            customdata=sub[
                [
                    "evidence",
                    "status",
                    "finding",
                    "basis",
                    "decision_role",
                ]
            ].values,

            hovertemplate=(
                "<b>%{customdata[0]}</b>"
                "<br><br>"
                "<b>Role:</b> %{customdata[4]}"
                "<br>"
                "<b>Status:</b> %{customdata[1]}"
                "<br><br>"
                "<b>Finding:</b><br>%{customdata[2]}"
                "<br><br>"
                "<b>Evidence / tool:</b><br>%{customdata[3]}"
                "<extra></extra>"
            ),
        )
    )


# ============================================================
# Y LABELS
# ============================================================

tickvals = df["y"].tolist()

ticktext = df["evidence"].tolist()


# ============================================================
# DOMAIN SEPARATORS
# ============================================================

shapes = []


for i in range(
    len(df) - 1
):

    current_domain = str(
        df.loc[
            i,
            "domain"
        ]
    )

    next_domain = str(
        df.loc[
            i + 1,
            "domain"
        ]
    )

    if current_domain != next_domain:

        separator_y = (
            df.loc[
                i,
                "y"
            ]
            -
            0.5
        )

        shapes.append(
            dict(
                type="line",

                x0=-0.45,
                x1=3.45,

                y0=separator_y,
                y1=separator_y,

                line=dict(
                    color="#D9DEE3",
                    width=1,
                ),
            )
        )


# ============================================================
# DECISION REGION BACKGROUNDS
# ============================================================

ROLE_BACKGROUNDS = [
    "#F0F8F3",
    "#FFF7E8",
    "#FCF0EF",
    "#F8F1EB",
]


for i, color in enumerate(
    ROLE_BACKGROUNDS
):

    shapes.append(
        dict(
            type="rect",

            x0=i - 0.42,
            x1=i + 0.42,

            y0=-0.8,
            y1=len(df) - 0.2,

            fillcolor=color,

            opacity=0.50,

            line=dict(
                width=0
            ),

            layer="below",
        )
    )


# ============================================================
# LAYOUT
# ============================================================

fig.update_layout(

    title=dict(

        text=(
            "<b>Integrated evidence landscape</b>"
            "<br>"
            "<sup>"
            "Position indicates the role of each result in the decision — "
            "not quantitative evidence strength"
            "</sup>"
        ),

        x=0.5,
        xanchor="center",
    ),

    height=680,

    margin=dict(
        l=260,
        r=35,
        t=90,
        b=85,
    ),

    paper_bgcolor="white",

    plot_bgcolor="white",

    font=dict(
        size=12,
        color="#18212B",
    ),

    xaxis=dict(

        tickmode="array",

        tickvals=[
            0,
            1,
            2,
            3,
        ],

        ticktext=[
            "<b>SUPPORTS<br>HYPOTHESIS</b>",
            "<b>REFINES<br>MODEL</b>",
            "<b>NO ADDITIONAL<br>SUPPORT</b>",
            "<b>REQUIRES<br>EXPERIMENT</b>",
        ],

        range=[
            -0.48,
            3.48,
        ],

        side="top",

        tickfont=dict(
            size=11,
        ),

        showgrid=False,

        zeroline=False,

        fixedrange=True,
    ),

    yaxis=dict(

        tickmode="array",

        tickvals=tickvals,

        ticktext=ticktext,

        tickfont=dict(
            size=10,
        ),

        showgrid=False,

        zeroline=False,

        fixedrange=True,
    ),

    legend=dict(

        orientation="h",

        y=-0.10,

        x=0.5,

        xanchor="center",

        title=None,

        font=dict(
            size=10,
        ),
    ),

    shapes=shapes,

    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial",
    ),
)


fig.show()


# ============================================================
# SAVE INTERACTIVE FIGURE
# ============================================================

OUTPUT_HTML = Path(
    "/content/"
    "Figure_16_integrated_evidence_landscape.html"
)


fig.write_html(
    OUTPUT_HTML,
    include_plotlyjs="cdn",
)


# ============================================================
# FINAL DECISION CARD
# ============================================================

display(
    HTML(
        """
        <div style="
            border:2px solid #2E8B57;
            background:#F1F8F4;
            border-radius:12px;
            padding:17px 22px;
            margin-top:10px;
            text-align:center;
        ">

        <div style="
            font-size:12px;
            font-weight:700;
            color:#2E8B57;
            letter-spacing:0.7px;
        ">
        FINAL TRANSLATIONAL DECISION
        </div>

        <div style="
            font-size:22px;
            font-weight:800;
            margin-top:5px;
            color:#18212B;
        ">
        ADVANCE TO DISEASE-RELEVANT PROOF-OF-MECHANISM
        </div>

        <div style="
            max-width:1000px;
            margin:9px auto 0 auto;
            font-size:14px;
            line-height:1.5;
            color:#4F5B66;
        ">

        Independent human disease biology, fibroblast-state replication,
        network medicine, functional DPP4 perturbation and human
        pharmacology converge on a testable repurposing opportunity.

        <br><br>

        The critical remaining gate is
        <b>human dermal DPP4 target engagement and suppression of
        disease-relevant fibroblast fibrotic activity</b>.

        </div>

        <div style="
            margin-top:10px;
            color:#A34D47;
            font-size:13px;
            font-weight:700;
        ">
        This is not a clinical efficacy claim.
        </div>

        </div>
        """
    )
)


# ============================================================
# CONCISE FINAL CONCLUSION
# ============================================================

display(
    HTML(
        """
        <div style="
            border-left:4px solid #666;
            padding:14px 18px;
            margin-top:14px;
            line-height:1.55;
        ">

        <b>Integrated conclusion</b><br>

        The evidence supports a
        <b>mechanistically grounded and pharmacologically plausible
        opportunity to test vildagliptin for cutaneous fibrosis in
        systemic sclerosis</b>.

        <br><br>

        Human SSc datasets define a reproducible fibroblast/ECM context
        for DPP4, downstream fibrotic programs track mRSS, experimental
        perturbation provides causal antifibrotic support, and human
        pharmacology supports systemic target engagement.

        <br><br>

        The analyses also refine the original model:
        DPP4 is not globally increased, is not a positive severity
        biomarker, and does not define a simple linear fibroblast
        trajectory or the state with maximal canonical TGFβ signaling.

        <br><br>

        LINCS reversal and human genetics did not add independent
        positive support and are retained as explicit limitations.

        <br><br>

        Human dermal pharmacology has been
        <b>partially de-risked</b>:
        the required skin exposure has been quantified, but actual
        dermal exposure and DPP4 target engagement remain to be measured.

        <br><br>

        <b>
        The project therefore advances from computational/mechanistic
        validation to disease-relevant experimental proof-of-mechanism.
        </b>

        </div>
        """
    )
)


print(
    "\nInteractive evidence landscape saved to:"
)

print(
    OUTPUT_HTML
)