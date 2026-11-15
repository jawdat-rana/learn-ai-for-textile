"""For the course owner: rebuild each .ipynb from its .py file.

The .py files are the source. Cells start with "# %%"; "# %% [markdown]"
cells become text. Run: python tools/make_notebooks.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ["module-1-product-lca/analysis/product_lca.py",
           "module-2-material-substitution/analysis/material_compare.py",
           "part-2-advanced/agents/lca_agents.py"]

def cells_from(text):
    cells, current, kind = [], [], None
    for line in text.splitlines():
        if line.startswith("# %%"):
            if kind:
                cells.append((kind, current))
            kind, current = ("markdown" if "[markdown]" in line else "code"), []
            continue
        current.append(line[2:] if kind == "markdown" and line.startswith("# ") else
                       "" if kind == "markdown" and line == "#" else line)
    if kind:
        cells.append((kind, current))
    out = []
    for kind, lines in cells:
        while lines and not lines[-1].strip():
            lines.pop()
        src = [l + "\n" for l in lines]
        if src:
            src[-1] = src[-1].rstrip("\n")
        cell = {"cell_type": kind, "id": f"cell-{len(out) + 1}", "metadata": {}, "source": src}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        out.append(cell)
    return out

for rel in SCRIPTS:
    py = ROOT / rel
    nb = {"cells": cells_from(py.read_text()), "nbformat": 4, "nbformat_minor": 5,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"}, "colab": {"provenance": []}}}
    py.with_suffix(".ipynb").write_text(json.dumps(nb, indent=1) + "\n")
    print("wrote", py.with_suffix(".ipynb").relative_to(ROOT), len(nb["cells"]), "cells")
