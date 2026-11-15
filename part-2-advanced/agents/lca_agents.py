# %% [markdown]
# # A team of AI agents for a product footprint review
#
# Three agents work together on the Module 1 lifecycle model:
#
# | Agent | Job | Tools |
# |---|---|---|
# | **Planner** | Turns the brief into scenarios to test, and writes the final memo | none |
# | **Analyst** | Runs the lifecycle model for each scenario and reports results | `run_lca_scenario` |
# | **Reviewer** | Checks every number against the model log, and checks the wording for over-claiming | the log |
#
# The Reviewer plays the role of an ISO 14044 critical reviewer: it checks
# evidence, not the other agents' words.
#
# It uses Google's **Gemini API free tier** (no credit card). Without a key it
# runs in **practice mode** with stand-in answers but real model results, so
# you can see how the hand-offs work first. Written by AI from the prompt in
# `part-2-advanced/exercise-3-agent-team-in-colab.md`.
#
# Run each cell in order (Shift+Enter in Google Colab).

# %%
# STEP 1: Install the Gemini library (Colab only needs this once per session).
# On your own computer instead run: pip install google-genai pandas
try:
    from google import genai
    from google.genai import types
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "google-genai"], check=False)
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        genai = None

# %%
# STEP 2: Your API key. Never paste the key into the code or into GitHub.
# In Colab: click the key icon on the left (Secrets), add GEMINI_API_KEY,
# and switch on "Notebook access". No key = practice mode.
import os
API_KEY = os.environ.get("GEMINI_API_KEY")
try:
    from google.colab import userdata
    API_KEY = userdata.get("GEMINI_API_KEY")
except Exception:
    pass

# Use a current free "flash" model. If you get a "model not found" error,
# check the model list in Google AI Studio and change this name.
MODEL = "gemini-2.5-flash"
PRACTICE_MODE = not (API_KEY and genai)
client = None if PRACTICE_MODE else genai.Client(api_key=API_KEY)
print("Practice mode (no AI calls)" if PRACTICE_MODE else f"Live mode with {MODEL}")

# %%
# STEP 3: The tool. This is the Module 1 lifecycle model, wrapped as a
# function the Analyst agent is allowed to call. Every call is written to
# MODEL_LOG so the Reviewer can check the Analyst's numbers.
from pathlib import Path
import pandas as pd

BASE_URL = ("https://raw.githubusercontent.com/jawdat-rana/learn-ai-for-textile/"
            "main/module-1-product-lca/data/")

def load(name):
    candidates = [Path(name)]
    try:
        candidates.insert(0, Path(__file__).resolve().parents[2] / "module-1-product-lca" / "data" / name)
    except NameError:
        pass
    for p in candidates:
        if p.exists():
            return pd.read_csv(p)
    return pd.read_csv(BASE_URL + name)

products, bom, legs = load("products.csv"), load("bill_of_materials.csv"), load("transport_legs.csv")
factors, grid = load("emission_factors.csv"), load("grid_intensity.csv")
F = dict(zip(factors.factor_id, factors.value))
GRID = dict(zip(grid.country, grid.kg_co2e_per_kwh))
HEAT_FUEL = dict(zip(grid.country, grid.heat_fuel))
MODEL_LOG = []

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

def base_recipe(pid):
    rows = bom[bom.product_id == pid]
    recipe = dict(zip(rows.material, rows.share_pct / 100))
    gap = 1 - sum(recipe.values())
    if abs(gap) > 0.001:  # same cautious rule as Module 1
        recipe["FIB_PES"] = recipe.get("FIB_PES", 0) + gap
    return recipe

def run_lca_scenario(product_id: str, fibre: str = "", mill_country: str = "",
                     ship_by: str = "", cut_waste_pct: int = 0) -> str:
    """Run the screening lifecycle model (kg CO2e per garment, cradle to grave) for one product.

    Args:
        product_id: P01 to P06 (P01 Performance T-shirt, P02 Classic cotton T-shirt, P03 Fleece jacket,
            P04 Sports leggings, P05 Workwear trousers, P06 Swim shorts).
        fibre: Leave empty to keep the design, or one of: virgin polyester, recycled polyester,
            conventional cotton, organic cotton (100% of the garment).
        mill_country: Leave empty to keep, or where yarn, fabric and dyeing happen: China, Bangladesh,
            India, Vietnam, Turkey, Pakistan, Portugal, Italy, Germany, Switzerland.
        ship_by: Leave empty to keep, or "sea" or "air" for the long-distance leg.
        cut_waste_pct: 0 to keep, or the new cutting waste in percent (5-30).

    Returns:
        The total and each stage, before and after the changes, with the % change.
    """
    p = products.set_index("product_id").loc[product_id].to_dict()
    recipe, product_legs = base_recipe(product_id), legs[legs.product_id == product_id].to_dict("records")
    before = footprint(p, recipe, product_legs, F, GRID, HEAT_FUEL)
    fibres = {"virgin polyester": "FIB_PES", "recycled polyester": "FIB_RPES",
              "conventional cotton": "FIB_CO", "organic cotton": "FIB_OCO"}
    if fibre:
        recipe = {fibres[fibre.lower()]: 1.0}
        p["yarn_type"] = "staple" if "cotton" in fibre.lower() else "filament"
    if mill_country:
        p["mill_country"] = mill_country
    if cut_waste_pct:
        p["cut_waste_pct"] = cut_waste_pct
    if ship_by:  # flight routes are roughly 55% of the sea distance
        product_legs = [{**l, "mode": ship_by,
                         "distance_km": l["distance_km"] * (0.55 if ship_by == "air" and l["mode"] == "sea" else
                                                            1.8 if ship_by == "sea" and l["mode"] == "air" else 1)}
                        if l["mode"] in ("sea", "air") else l for l in product_legs]
    after = footprint(p, recipe, product_legs, F, GRID, HEAT_FUEL)
    tb, ta = sum(before.values()), sum(after.values())
    lines = [f"{product_id} {p['product_name']} | before {tb:.2f} | after {ta:.2f} | change {100 * (ta - tb) / tb:+.1f}%"]
    lines += [f"  {s}: {before[s]:.2f} -> {after[s]:.2f}" for s in STAGES]
    result = "\n".join(lines)
    MODEL_LOG.append({"settings": dict(product_id=product_id, fibre=fibre, mill_country=mill_country,
                                       ship_by=ship_by, cut_waste_pct=cut_waste_pct), "result": result})
    return result

print(run_lca_scenario("P04", ship_by="sea"))
MODEL_LOG.clear()

# %%
# STEP 4: The agents. An agent here is just: instructions + (optional) tools.
# Read the instructions: this is where the real design work is, and it's in English.
BRIEF = """Next season the product team wants to cut the screening footprint of
P01 Performance T-shirt and P04 Sports leggings by at least 25% each. Options on
the table: recycled polyester (P01 only), moving dyeing and finishing to Portugal
or Turkey, shipping by sea instead of air, and cutting waste down to 10%.
Marketing would like to say "25% lower carbon" on the hangtag. The steering
committee wants to know which combination reaches -25% and what we can say publicly."""

AGENTS = {
    "Planner": dict(tools=[], instructions="""You lead a product sustainability review.
Turn the brief into an analysis plan: 4 to 6 scenarios to test, each with exact
settings for run_lca_scenario (product_id, fibre, mill_country, ship_by,
cut_waste_pct), including single changes and combinations. Say what question
each scenario answers. Be concise. Do not invent results."""),
    "Analyst": dict(tools=[run_lca_scenario], instructions="""You are an LCA analyst.
For EVERY scenario in the plan, call run_lca_scenario with its settings.
Report each result as a compact table, copying numbers exactly from the tool.
Then say which scenarios reach -25% for each product. Never estimate a number
yourself; if you didn't run it, say so. These are screening results (not
ISO 14040/44), so say that once."""),
    "Reviewer": dict(tools=[], instructions="""You are a sceptical critical reviewer of LCA work.
You get the analyst's report and the MODEL LOG of what was actually run.
Check: (1) every number in the report appears in the log, (2) every planned
scenario was run, (3) the conclusions follow from the numbers, (4) the report
does not over-claim: no public claims such as "25% lower carbon" from a
screening model, no implied certainty. Reply with APPROVED on the first line if
it passes, or REVISE on the first line followed by a numbered list of fixes."""),
}

def ask(agent, message):
    """Send a message to one agent and return its reply."""
    spec = AGENTS[agent]
    if PRACTICE_MODE:
        return practice_reply(agent, message)
    config = types.GenerateContentConfig(system_instruction=spec["instructions"],
                                         tools=spec["tools"] or None, temperature=0.2)
    return client.models.generate_content(model=MODEL, contents=message, config=config).text

PRACTICE_RUNS = [dict(product_id="P01", fibre="recycled polyester"),
                 dict(product_id="P01", mill_country="Portugal"),
                 dict(product_id="P01", fibre="recycled polyester", mill_country="Portugal", cut_waste_pct=10),
                 dict(product_id="P04", ship_by="sea"),
                 dict(product_id="P04", ship_by="sea", mill_country="Turkey")]

def practice_reply(agent, message):
    """Stand-in answers so you can see the hand-offs without an API key."""
    if agent == "Planner" and "final memo" not in message:
        return "PLAN (practice mode)\n" + "\n".join(f"{i}. {r}" for i, r in enumerate(PRACTICE_RUNS, 1))
    if agent == "Analyst":
        return "REPORT (practice mode: model results are real, wording is canned)\n\n" + "\n\n".join(
            f"Scenario {i}: {r}\n" + run_lca_scenario(**r) for i, r in enumerate(PRACTICE_RUNS, 1))
    if agent == "Reviewer":
        return "APPROVED (practice mode: a real reviewer would check each number against the log and the wording)"
    return "MEMO (practice mode): with a real API key the Planner writes the steering committee memo here."

def show(title, text):
    print("\n" + "=" * 80 + f"\n{title}\n" + "=" * 80 + f"\n{text}")

# %%
# STEP 5: Run the team. Planner -> Analyst -> Reviewer (-> one revision) -> Planner.
plan = ask("Planner", f"BRIEF:\n{BRIEF}")
show("PLANNER: analysis plan", plan)

report = ask("Analyst", f"BRIEF:\n{BRIEF}\n\nPLAN:\n{plan}")
show("ANALYST: results", report)

def log_text():
    return "\n\n".join(f"Run {i}: {r['settings']}\n{r['result']}" for i, r in enumerate(MODEL_LOG, 1))

review = ask("Reviewer", f"PLAN:\n{plan}\n\nANALYST REPORT:\n{report}\n\nMODEL LOG:\n{log_text()}")
show("REVIEWER: verdict", review)

if review.strip().upper().startswith("REVISE"):
    report = ask("Analyst", f"BRIEF:\n{BRIEF}\n\nPLAN:\n{plan}\n\nYOUR LAST REPORT:\n{report}\n\n"
                            f"REVIEWER FEEDBACK:\n{review}\n\nFix every point and send the full revised report.")
    show("ANALYST: revised results", report)
    review = ask("Reviewer", f"PLAN:\n{plan}\n\nANALYST REPORT:\n{report}\n\nMODEL LOG:\n{log_text()}")
    show("REVIEWER: second verdict", review)

memo = ask("Planner", f"Write the final memo for the steering committee (under 300 words): "
                      f"which combination reaches -25% for each product, trade-offs, what we can and "
                      f"cannot say publicly, and what data to collect next. Use only numbers from the "
                      f"approved report.\n\nREPORT:\n{report}\n\nREVIEWER VERDICT:\n{review}")
show("PLANNER: final memo", memo)

# %%
# STEP 6: Look under the hood. How many scenarios did the team actually run?
print(f"The Analyst called the model {len(MODEL_LOG)} times:")
for r in MODEL_LOG:
    print(" ", r["settings"])
