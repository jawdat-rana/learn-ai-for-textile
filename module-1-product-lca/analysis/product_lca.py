# %% [markdown]
# # Product lifecycle screening (cradle to grave)
#
# This code was written by an AI from the plain-English prompt in
# `module-1-product-lca/prompts.md` (Prompt 4). A human then read the
# explanation, checked one product by hand and asked the AI for fixes.
#
# It estimates the **carbon footprint (kg CO2e)** of six made-up textile
# products across their whole life: raw materials, yarn, fabric, dyeing and
# finishing, garment making, transport, use (washing and drying) and end of life.
#
# **This is a screening-level estimate, not an ISO 14040/44 study.** It uses
# rounded public emission factors (see `data/emission_factors.csv` and
# `SOURCES.md`) and simple assumptions. Use it to find hotspots and ask better
# questions, not to make public claims.
#
# **You do not need to understand every line.** Run each cell in order
# (Shift+Enter in Google Colab). If something breaks, copy the error into your
# AI chat and ask: "What does this error mean and how do I fix it?"

# %%
# STEP 1: Load the five data files.
# It tries a local copy first, then downloads the sample files from GitHub.
from pathlib import Path
import pandas as pd

# If you copied this course and changed the data, replace "jawdat-rana"
# with your own GitHub username.
DATA_URL = ("https://raw.githubusercontent.com/jawdat-rana/learn-ai-for-textile/"
            "main/module-1-product-lca/data/")

def load(name):
    candidates = [Path(name), Path("data") / name]
    try:  # works when you run the .py file on a computer
        candidates.insert(0, Path(__file__).resolve().parent.parent / "data" / name)
    except NameError:  # Colab notebooks have no __file__
        pass
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    return pd.read_csv(DATA_URL + name)

products = load("products.csv")
bom = load("bill_of_materials.csv")
legs = load("transport_legs.csv")
factors = load("emission_factors.csv")
grid = load("grid_intensity.csv")

F = dict(zip(factors.factor_id, factors.value))             # factor_id -> value
GRID = dict(zip(grid.country, grid.kg_co2e_per_kwh))         # country -> kg CO2e per kWh
HEAT_FUEL = dict(zip(grid.country, grid.heat_fuel))          # country -> gas or coal
print(f"Loaded {len(products)} products, {len(factors)} factors, {len(grid)} countries")
products

# %%
# STEP 2: Check the data before calculating anything.
# Bills of materials should add up to 100%. If one doesn't, we fill the gap
# with virgin polyester (a cautious assumption) and flag it, so someone fixes the data.
FILL_MATERIAL = "FIB_PES"
problems = []
recipes = {}
for pid in products.product_id:
    rows = bom[bom.product_id == pid]
    recipe = dict(zip(rows.material, rows.share_pct / 100))
    total = sum(recipe.values())
    if abs(total - 1) > 0.001:
        problems.append(f"{pid}: materials add up to {total:.0%}. Gap filled with virgin polyester.")
        recipe[FILL_MATERIAL] = recipe.get(FILL_MATERIAL, 0) + (1 - total)
    for m in recipe:
        if m not in F:
            problems.append(f"{pid}: no emission factor for {m}")
    recipes[pid] = recipe
for _, p in products.iterrows():
    for c in (p.mill_country, p.make_country, p.market):
        if c not in GRID:
            problems.append(f"{p.product_id}: no grid factor for {c}")
for _, leg in legs.iterrows():
    if "TR_" + leg["mode"].upper() not in F:
        problems.append(f"{leg.product_id}: unknown transport mode {leg['mode']}")
print("Data problems found:" if problems else "No data problems found.")
for msg in problems:
    print(" -", msg)

# %%
# STEP 3: The lifecycle model, one stage at a time.
# Work backwards from the finished garment: cutting waste, finishing losses
# and spinning losses mean we need more fibre than the garment weighs.

STAGES = ["Raw materials", "Yarn", "Fabric", "Dyeing and finishing",
          "Garment making", "Transport", "Use", "End of life"]
INCINERATE = {"FIB_PES": "EOL_INC_PES", "FIB_RPES": "EOL_INC_PES", "FIB_PESBD": "EOL_INC_PES",
              "FIB_PA": "EOL_INC_PA", "FIB_EL": "EOL_INC_EL", "FIB_CO": "EOL_INC_CO", "FIB_OCO": "EOL_INC_CO"}
LANDFILL = {"FIB_PES": "EOL_LF_SYN", "FIB_RPES": "EOL_LF_SYN", "FIB_PA": "EOL_LF_SYN", "FIB_EL": "EOL_LF_SYN",
            "FIB_PESBD": "EOL_LF_PESBD", "FIB_CO": "EOL_LF_NAT", "FIB_OCO": "EOL_LF_NAT"}

def material_flow(p, F):
    """Kilograms needed at each step for one garment."""
    garment = p["garment_mass_g"] / 1000
    finished_fabric = garment / (1 - p["cut_waste_pct"] / 100)
    greige_fabric = finished_fabric / (1 - F["LOSS_FINISH"] / 100)
    yarn = greige_fabric / (1 - F["LOSS_FABRIC"] / 100)
    yarn_loss = F["LOSS_YARN_STAPLE"] if p["yarn_type"] == "staple" else F["LOSS_YARN_FILAMENT"]
    fibre = yarn / (1 - yarn_loss / 100)
    return dict(garment=garment, finished_fabric=finished_fabric,
                greige_fabric=greige_fabric, yarn=yarn, fibre=fibre)

def footprint(p, recipe, product_legs, F, GRID, HEAT_FUEL):
    """kg CO2e per garment for each life cycle stage."""
    kg = material_flow(p, F)
    mill, make, market = GRID[p["mill_country"]], GRID[p["make_country"]], GRID[p["market"]]
    fuel = F["FUEL_COAL"] if HEAT_FUEL[p["mill_country"]] == "coal" else F["FUEL_GAS"]
    yarn_kwh = F["YARN_STAPLE"] if p["yarn_type"] == "staple" else F["YARN_FILAMENT"]
    fabric_kwh = F["FAB_WOVEN"] if p["construction"] == "woven" else F["FAB_KNIT"]
    packaging = F["PACK_LDPE_KG"] + F["PACK_CARD_KG"]

    out = {}
    out["Raw materials"] = sum(kg["fibre"] * share * F[m] for m, share in recipe.items())
    out["Yarn"] = kg["yarn"] * yarn_kwh * mill
    out["Fabric"] = kg["greige_fabric"] * fabric_kwh * mill
    out["Dyeing and finishing"] = kg["greige_fabric"] * (
        F["WET_ELEC"] * mill + F["WET_HEAT"] / F["BOILER_EFF"] * fuel)
    out["Garment making"] = (kg["garment"] * F["MAKE_ELEC"] * make
                             + F["PACK_LDPE_KG"] * F["PACK_LDPE"] + F["PACK_CARD_KG"] * F["PACK_CARD"])
    transport = 0.0
    for leg in product_legs:
        cargo_kg = kg["fibre"] if leg["cargo"] == "fibre" else kg["garment"] + packaging
        transport += cargo_kg / 1000 * leg["distance_km"] * F["TR_" + leg["mode"].upper()]
    out["Transport"] = transport
    share_of_load = kg["garment"] / F["USE_LOAD"]
    kwh_per_wash = F["USE_WASH"] + p["tumble_dry_share_pct"] / 100 * F["USE_DRY"]
    out["Use"] = p["washes_in_life"] * share_of_load * kwh_per_wash * market
    out["End of life"] = sum(
        kg["garment"] * share * (p["incineration_pct"] / 100 * F[INCINERATE[m]]
                                 + p["landfill_pct"] / 100 * F[LANDFILL[m]])
        for m, share in recipe.items())
    return out

def product_inputs(pid):
    p = products.set_index("product_id").loc[pid].to_dict()
    product_legs = legs[legs.product_id == pid].to_dict("records")
    return p, recipes[pid], product_legs

# %%
# STEP 4: Calculate every product, by stage.
results = []
for pid in products.product_id:
    p, recipe, product_legs = product_inputs(pid)
    stages = footprint(p, recipe, product_legs, F, GRID, HEAT_FUEL)
    results.append({"product_id": pid, "product_name": p["product_name"], **stages,
                    "total_kg_co2e": sum(stages.values()),
                    "kg_co2e_per_kg_garment": sum(stages.values()) / (p["garment_mass_g"] / 1000)})
table = pd.DataFrame(results).round(3)
print(table[["product_id", "product_name", "total_kg_co2e", "kg_co2e_per_kg_garment"]].to_string(index=False))

out_dir = Path("output")
try:
    out_dir = Path(__file__).resolve().parent.parent / "output"
except NameError:
    pass
out_dir.mkdir(exist_ok=True)
table.to_csv(out_dir / "footprint_by_stage.csv", index=False)
table

# %%
# STEP 5: Hotspots. Which stages matter most for each product?
import matplotlib.pyplot as plt

colours = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#7d5bd0", "#d03b8a", "#4bb3c9", "#7a7974"]
fig, ax = plt.subplots(figsize=(9, 4.8))
left = [0.0] * len(table)
labels = [f"{r.product_id} {r.product_name}" for r in table.itertuples()]
for stage, colour in zip(STAGES, colours):
    ax.barh(labels, table[stage], left=left, color=colour, label=stage)
    left = [l + v for l, v in zip(left, table[stage])]
ax.invert_yaxis()
ax.set_xlabel("kg CO2e per garment (screening estimate)")
ax.set_title("Where each product's footprint comes from")
ax.legend(ncol=4, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.42), frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig(out_dir / "hotspots.png", dpi=150)
plt.show()

for r in results:
    top = max(STAGES, key=lambda s: r[s])
    print(f"{r['product_id']} {r['product_name']}: biggest stage is {top} "
          f"({r[top] / r['total_kg_co2e']:.0%} of {r['total_kg_co2e']:.2f} kg CO2e)")

# %%
# STEP 6: Sensitivity. How much does the answer move if each factor is at the
# low or high end of its published range? Big bars = numbers worth checking first.
def total_with(pid, factor_id, value):
    F2 = dict(F)
    F2[factor_id] = value
    p, recipe, product_legs = product_inputs(pid)
    return sum(footprint(p, recipe, product_legs, F2, GRID, HEAT_FUEL).values())

def sensitivity(pid, top_n=8):
    base = table.set_index("product_id").loc[pid, "total_kg_co2e"]
    rows = []
    for f in factors.itertuples():
        lo, hi = total_with(pid, f.factor_id, f.low), total_with(pid, f.factor_id, f.high)
        if abs(hi - lo) > 1e-9:
            rows.append(dict(factor_id=f.factor_id, item=f.item, confidence=f.confidence,
                             low_total=lo, high_total=hi, swing=abs(hi - lo)))
    return base, pd.DataFrame(rows).sort_values("swing", ascending=False).head(top_n)

base, sens = sensitivity("P01")
fig, ax = plt.subplots(figsize=(9, 4))
for i, r in enumerate(sens.itertuples()):
    lo, hi = sorted((r.low_total, r.high_total))
    ax.barh(i, hi - lo, left=lo, color="#2a78d6" if r.confidence != "Low" else "#eb6834")
ax.axvline(base, color="#0b0b0b", lw=1)
ax.set_yticks(range(len(sens)), [f"{r.item[:45]} ({r.confidence})" for r in sens.itertuples()], fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Total kg CO2e per garment if this factor is at its low or high value")
ax.set_title(f"P01 Performance T-shirt: what moves the answer (base {base:.2f} kg CO2e)")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig(out_dir / "sensitivity_P01.png", dpi=150)
plt.show()
sens.round(2)

# %%
# STEP 7: What-if scenarios, in plain English. Each one changes one thing.
def scenario(pid, label, product_changes=None, factor_changes=None, recipe=None, product_legs=None):
    p, base_recipe, base_legs = product_inputs(pid)
    p = {**p, **(product_changes or {})}
    F2 = {**F, **(factor_changes or {})}
    before = table.set_index("product_id").loc[pid, "total_kg_co2e"]
    after = sum(footprint(p, recipe or base_recipe, product_legs or base_legs, F2, GRID, HEAT_FUEL).values())
    return dict(product_id=pid, scenario=label, before=round(before, 2), after=round(after, 2),
                change_pct=round(100 * (after - before) / before, 1))

p04_sea = [dict(cargo="fibre", mode="truck", distance_km=500), dict(cargo="garment", mode="truck", distance_km=50),
           dict(cargo="garment", mode="sea", distance_km=18500), dict(cargo="garment", mode="truck", distance_km=500)]
whatifs = pd.DataFrame([
    scenario("P01", "Switch to recycled polyester", recipe={"FIB_RPES": 1.0}),
    scenario("P01", "Dye and finish in Portugal instead of China", product_changes={"mill_country": "Portugal"}),
    scenario("P02", "Switch to organic cotton", recipe={"FIB_OCO": 1.0}),
    scenario("P02", "Customer never tumble dries", product_changes={"tumble_dry_share_pct": 0}),
    scenario("P03", "Cut waste from 18% to 10%", product_changes={"cut_waste_pct": 10}),
    scenario("P04", "Ship by sea instead of air", product_legs=p04_sea),
    scenario("P05", "Garment lasts 150 washes instead of 100 (per wash this is better; per garment it is worse)",
             product_changes={"washes_in_life": 150}),
])
print(whatifs.to_string(index=False))
whatifs

# %%
# STEP 8: The headline numbers for your summary (copy these into your AI chat).
print("SCREENING-LEVEL RESULTS (not an ISO 14040/44 study; factors are rounded public values)")
for r in results:
    stage_share = ", ".join(f"{s} {r[s] / r['total_kg_co2e']:.0%}" for s in STAGES if r[s] / r["total_kg_co2e"] >= 0.1)
    print(f"- {r['product_id']} {r['product_name']}: {r['total_kg_co2e']:.2f} kg CO2e per garment "
          f"({r['kg_co2e_per_kg_garment']:.1f} per kg). Main stages: {stage_share}")
print("Data problems:", "; ".join(problems) if problems else "none")
