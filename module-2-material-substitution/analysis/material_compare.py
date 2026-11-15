# %% [markdown]
# # Material substitution: which fibre for our performance T-shirt?
#
# This code was written by an AI from the plain-English prompts in
# `module-2-material-substitution/prompts.md` (Prompt 3). It reuses the
# lifecycle model from Module 1 and compares six material options for the
# same T-shirt (P01): climate impact per garment AND per wear, plus things a
# carbon number can't show (microplastics, water, end of life, evidence).
#
# **Screening level only.** The fibre factors are rounded public values with
# wide ranges, and durability (washes in life) is an assumption you should
# test with real wear data. Run each cell in order (Shift+Enter in Colab).

# %%
# STEP 1: Load Module 1's data (factors, countries, the T-shirt) and the options.
from pathlib import Path
import pandas as pd

BASE = "https://raw.githubusercontent.com/jawdat-rana/learn-ai-for-textile/main/"

def load(folder, name):
    candidates = [Path(name), Path("data") / name]
    try:
        candidates.insert(0, Path(__file__).resolve().parents[2] / folder / "data" / name)
    except NameError:
        pass
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    return pd.read_csv(BASE + folder + "/data/" + name)

factors = load("module-1-product-lca", "emission_factors.csv")
grid = load("module-1-product-lca", "grid_intensity.csv")
products = load("module-1-product-lca", "products.csv")
legs = load("module-1-product-lca", "transport_legs.csv")
options = load("module-2-material-substitution", "material_options.csv")
beyond = load("module-2-material-substitution", "beyond_carbon.csv")

F = dict(zip(factors.factor_id, factors.value))
GRID = dict(zip(grid.country, grid.kg_co2e_per_kwh))
HEAT_FUEL = dict(zip(grid.country, grid.heat_fuel))
BASE_PRODUCT = products.set_index("product_id").loc["P01"].to_dict()
BASE_LEGS = legs[legs.product_id == "P01"].to_dict("records")
print("Base product:", BASE_PRODUCT["product_name"], "| options:", len(options))
options

# %%
# STEP 2: The lifecycle model, copied unchanged from Module 1.
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

def parse_materials(text):
    """'FIB_RPES:50;FIB_OCO:50' -> {'FIB_RPES': 0.5, 'FIB_OCO': 0.5}"""
    return {m: float(s) / 100 for m, s in (part.split(":") for part in text.split(";"))}

# %%
# STEP 3: Calculate each option, per garment and per wear.
# We assume one wear per wash (an assumption: change WEARS_PER_WASH to test it).
WEARS_PER_WASH = 1.0

def option_product(opt):
    return {**BASE_PRODUCT, "garment_mass_g": opt["garment_mass_g"], "yarn_type": opt["yarn_type"],
            "washes_in_life": opt["washes_in_life"], "tumble_dry_share_pct": opt["tumble_dry_share_pct"]}

def option_total(opt, F):
    return sum(footprint(option_product(opt), parse_materials(opt["materials"]), BASE_LEGS, F, GRID, HEAT_FUEL).values())

rows = []
for opt in options.to_dict("records"):
    recipe = parse_materials(opt["materials"])
    stages = footprint(option_product(opt), recipe, BASE_LEGS, F, GRID, HEAT_FUEL)
    total = sum(stages.values())
    # Range: the fibre factors and their landfill factors at their low, then high values.
    lo_F, hi_F = dict(F), dict(F)
    for m in recipe:
        for fid in (m, LANDFILL[m]):
            lo_F[fid] = factors.set_index("factor_id").loc[fid, "low"]
            hi_F[fid] = factors.set_index("factor_id").loc[fid, "high"]
    wears = opt["washes_in_life"] * WEARS_PER_WASH
    low, high = option_total(opt, lo_F), option_total(opt, hi_F)
    fibre_kg = material_flow(option_product(opt), F)["fibre"]
    rows.append(dict(option_id=opt["option_id"], option_name=opt["option_name"],
                     kg_co2e_per_garment=total,
                     low=low, high=high, g_co2e_per_wear=1000 * total / wears,
                     low_per_wear=1000 * low / wears, high_per_wear=1000 * high / wears,
                     raw_materials=stages["Raw materials"], use=stages["Use"], end_of_life=stages["End of life"],
                     fibre_cost_eur=fibre_kg * opt["fibre_cost_eur_per_kg"]))
compare = pd.DataFrame(rows)
print(compare.round(2).to_string(index=False))

# %%
# STEP 4: Chart: climate impact per wear, with the range from fibre factors.
import matplotlib.pyplot as plt
c = compare.sort_values("g_co2e_per_wear")
fig, ax = plt.subplots(figsize=(9, 4))
ax.barh(c.option_name, c.g_co2e_per_wear, color="#2a78d6")
ax.errorbar(c.g_co2e_per_wear, range(len(c)), fmt="none", ecolor="#0b0b0b", capsize=3,
            xerr=[c.g_co2e_per_wear - c.low_per_wear, c.high_per_wear - c.g_co2e_per_wear])
ax.invert_yaxis()
ax.set_xlabel("g CO2e per wear (line = range from published fibre and landfill factors)")
ax.set_title("Performance T-shirt: climate impact per wear by material")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
out_dir = Path("output")
try:
    out_dir = Path(__file__).resolve().parent.parent / "output"
except NameError:
    pass
out_dir.mkdir(exist_ok=True)
plt.savefig(out_dir / "per_wear.png", dpi=150)
plt.show()

overlap = [(a.option_name, b.option_name) for a in c.itertuples() for b in c.itertuples()
           if a.option_id < b.option_id and a.low_per_wear <= b.high_per_wear and b.low_per_wear <= a.high_per_wear]
print(f"{len(overlap)} of 15 pairs have overlapping per-wear ranges, so this data can't separate them on climate:")
for a, b in overlap:
    print("  -", a, "vs", b)

# %%
# STEP 5: Beyond carbon. A weighted scorecard (5 = best). Change the weights to
# match what your company cares about; they must add up to 100.
WEIGHTS = {"climate": 35, "microplastics": 20, "water": 15, "end_of_life": 10, "cost": 20}
TRUST_SUPPLIER_CLAIM = False  # True = accept option E's biodegradability claim without test evidence

def to_1to5(values):
    """Lowest value scores 5, highest scores 1, straight line in between."""
    lo, hi = min(values), max(values)
    return [5.0 if hi == lo else 5 - 4 * (v - lo) / (hi - lo) for v in values]

card = compare[["option_id", "option_name"]].copy()
card["climate"] = to_1to5(compare.g_co2e_per_wear.tolist())
card["cost"] = to_1to5(compare.fibre_cost_eur.tolist())
b = beyond.set_index("option_id")
card["microplastics"] = [b.loc[i, "microplastics_1to5"] for i in card.option_id]
if TRUST_SUPPLIER_CLAIM:
    card.loc[card.option_id == "E", "microplastics"] = 4
card["water"] = [b.loc[i, "water_1to5"] for i in card.option_id]
card["end_of_life"] = [b.loc[i, "end_of_life_1to5"] for i in card.option_id]
card["evidence"] = [b.loc[i, "evidence_1to5"] for i in card.option_id]
card["weighted_score"] = sum(card[k] * w for k, w in WEIGHTS.items()) / sum(WEIGHTS.values())
card = card.sort_values("weighted_score", ascending=False).round(2)
card.to_csv(out_dir / "scorecard.csv", index=False)
compare.round(3).to_csv(out_dir / "option_comparison.csv", index=False)
print(card.to_string(index=False))
print("\nEvidence column is NOT in the score: read it before trusting a high score.")

# %%
# STEP 6: Headline for your summary (paste into your AI chat).
best_climate = compare.loc[compare.g_co2e_per_wear.idxmin()]
print("SCREENING-LEVEL COMPARISON for the performance T-shirt (not an ISO 14040/44 comparative assertion)")
for r in compare.sort_values("g_co2e_per_wear").itertuples():
    print(f"- {r.option_name}: {r.kg_co2e_per_garment:.2f} kg CO2e per garment "
          f"(range {r.low:.2f}-{r.high:.2f}), {r.g_co2e_per_wear:.0f} g per wear "
          f"(range {r.low_per_wear:.0f}-{r.high_per_wear:.0f}), fibre cost EUR {r.fibre_cost_eur:.2f}")
print(f"Lowest per wear: {best_climate.option_name}. Ranges overlap for {len(overlap)} of 15 pairs.")
print("Top of weighted scorecard:", card.iloc[0].option_name, f"({card.iloc[0].weighted_score})")
