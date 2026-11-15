// The lifecycle model used by both dashboards. Written by AI, explained in plain English.
// It is a line-by-line copy of the Python in module-1-product-lca/analysis/product_lca.py,
// so the website and the notebook give the same numbers (tools/check_numbers.js checks this).

const STAGES = ["Raw materials", "Yarn", "Fabric", "Dyeing and finishing",
  "Garment making", "Transport", "Use", "End of life"];
const STAGE_COLOURS = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)",
  "var(--s5)", "var(--s6)", "var(--s7)", "var(--s8)"];

// Which end-of-life factor applies to each fibre.
const INCINERATE = { FIB_PES: "EOL_INC_PES", FIB_RPES: "EOL_INC_PES", FIB_PESBD: "EOL_INC_PES",
  FIB_PA: "EOL_INC_PA", FIB_EL: "EOL_INC_EL", FIB_CO: "EOL_INC_CO", FIB_OCO: "EOL_INC_CO" };
const LANDFILL = { FIB_PES: "EOL_LF_SYN", FIB_RPES: "EOL_LF_SYN", FIB_PA: "EOL_LF_SYN", FIB_EL: "EOL_LF_SYN",
  FIB_PESBD: "EOL_LF_PESBD", FIB_CO: "EOL_LF_NAT", FIB_OCO: "EOL_LF_NAT" };

// 1. Turn the CSV rows into easy lookups: F.value[id], F.low[id], F.high[id].
function factorTables(rows) {
  const F = { value: {}, low: {}, high: {}, row: {} };
  rows.forEach(r => {
    F.value[r.factor_id] = +r.value; F.low[r.factor_id] = +r.low;
    F.high[r.factor_id] = +r.high; F.row[r.factor_id] = r;
  });
  return F;
}
function gridTables(rows) {
  const G = { kwh: {}, fuel: {} };
  rows.forEach(r => { G.kwh[r.country] = +r.kg_co2e_per_kwh; G.fuel[r.country] = r.heat_fuel; });
  return G;
}

// 2. Work backwards from the garment: cutting waste and process losses mean
//    we need more fabric, yarn and fibre than the garment weighs.
function materialFlow(p, F) {
  const garment = +p.garment_mass_g / 1000;
  const finished_fabric = garment / (1 - +p.cut_waste_pct / 100);
  const greige_fabric = finished_fabric / (1 - F.LOSS_FINISH / 100);
  const yarn = greige_fabric / (1 - F.LOSS_FABRIC / 100);
  const yarnLoss = p.yarn_type === "staple" ? F.LOSS_YARN_STAPLE : F.LOSS_YARN_FILAMENT;
  const fibre = yarn / (1 - yarnLoss / 100);
  return { garment, finished_fabric, greige_fabric, yarn, fibre };
}

// 3. kg CO2e for one garment, stage by stage. F is a plain {factor_id: value} object.
function footprint(p, recipe, legs, F, G) {
  const kg = materialFlow(p, F);
  const mill = G.kwh[p.mill_country], make = G.kwh[p.make_country], market = G.kwh[p.market];
  const fuel = G.fuel[p.mill_country] === "coal" ? F.FUEL_COAL : F.FUEL_GAS;
  const yarnKwh = p.yarn_type === "staple" ? F.YARN_STAPLE : F.YARN_FILAMENT;
  const fabricKwh = p.construction === "woven" ? F.FAB_WOVEN : F.FAB_KNIT;
  const packaging = F.PACK_LDPE_KG + F.PACK_CARD_KG;
  const out = {};
  out["Raw materials"] = Object.entries(recipe).reduce((s, [m, share]) => s + kg.fibre * share * F[m], 0);
  out["Yarn"] = kg.yarn * yarnKwh * mill;
  out["Fabric"] = kg.greige_fabric * fabricKwh * mill;
  out["Dyeing and finishing"] = kg.greige_fabric * (F.WET_ELEC * mill + F.WET_HEAT / F.BOILER_EFF * fuel);
  out["Garment making"] = kg.garment * F.MAKE_ELEC * make + F.PACK_LDPE_KG * F.PACK_LDPE + F.PACK_CARD_KG * F.PACK_CARD;
  out["Transport"] = legs.reduce((s, leg) => {
    const cargo = leg.cargo === "fibre" ? kg.fibre : kg.garment + packaging;
    return s + cargo / 1000 * +leg.distance_km * F["TR_" + leg.mode.toUpperCase()];
  }, 0);
  const shareOfLoad = kg.garment / F.USE_LOAD;
  const kwhPerWash = F.USE_WASH + +p.tumble_dry_share_pct / 100 * F.USE_DRY;
  out["Use"] = +p.washes_in_life * shareOfLoad * kwhPerWash * market;
  out["End of life"] = Object.entries(recipe).reduce((s, [m, share]) => s + kg.garment * share *
    (+p.incineration_pct / 100 * F[INCINERATE[m]] + +p.landfill_pct / 100 * F[LANDFILL[m]]), 0);
  return out;
}
const total = stages => Object.values(stages).reduce((a, b) => a + b, 0);

// 4. Bills of materials: shares that don't add up to 100% are filled with
//    virgin polyester and flagged (the same cautious rule as the Python).
function recipeFor(bomRows, pid, problems) {
  const recipe = {};
  bomRows.filter(r => r.product_id === pid).forEach(r => { recipe[r.material] = (recipe[r.material] || 0) + +r.share_pct / 100; });
  const sum = Object.values(recipe).reduce((a, b) => a + b, 0);
  if (Math.abs(sum - 1) > 0.001) {
    if (problems) problems.push(`${pid}: materials add up to ${Math.round(sum * 100)}%. Gap filled with virgin polyester.`);
    recipe.FIB_PES = (recipe.FIB_PES || 0) + (1 - sum);
  }
  return recipe;
}
// "FIB_RPES:50;FIB_OCO:50" -> {FIB_RPES: 0.5, FIB_OCO: 0.5}
const parseMaterials = text => Object.fromEntries(text.split(";").map(p => { const [m, s] = p.split(":"); return [m, +s / 100]; }));

// 5. Lowest value scores 5, highest scores 1 (used by the materials scorecard).
function to1to5(values) {
  const lo = Math.min(...values), hi = Math.max(...values);
  return values.map(v => hi === lo ? 5 : 5 - 4 * (v - lo) / (hi - lo));
}

if (typeof module !== "undefined") module.exports = { STAGES, INCINERATE, LANDFILL, factorTables, gridTables, materialFlow, footprint, total, recipeFor, parseMaterials, to1to5 };
