// For the course owner: checks the website's JavaScript model gives the same
// numbers as the Python notebooks. Run: node tools/check_numbers.js
// (after running both Python scripts, which write the output CSVs).
const fs = require("fs");
const path = require("path");
const L = require("../assets/lca.js");
const root = path.join(__dirname, "..");
function readCSV(rel) {
  const [head, ...lines] = fs.readFileSync(path.join(root, rel), "utf8").trim().split(/\r?\n/);
  const cols = head.split(",");
  return lines.map(l => Object.fromEntries(l.split(",").map((v, i) => [cols[i], v])));
}
const factors = L.factorTables(readCSV("module-1-product-lca/data/emission_factors.csv"));
const G = L.gridTables(readCSV("module-1-product-lca/data/grid_intensity.csv"));
const products = readCSV("module-1-product-lca/data/products.csv");
const bom = readCSV("module-1-product-lca/data/bill_of_materials.csv");
const legs = readCSV("module-1-product-lca/data/transport_legs.csv");
let failures = 0;
const check = (label, js, py) => {
  const ok = Math.abs(js - py) < 0.002;
  if (!ok) failures++;
  console.log(`${ok ? "ok  " : "FAIL"} ${label}: js ${js.toFixed(3)} python ${py.toFixed(3)}`);
};
const py1 = Object.fromEntries(readCSV("module-1-product-lca/output/footprint_by_stage.csv").map(r => [r.product_id, r]));
products.forEach(p => {
  const s = L.footprint(p, L.recipeFor(bom, p.product_id), legs.filter(l => l.product_id === p.product_id), factors.value, G);
  check(`${p.product_id} total`, L.total(s), +py1[p.product_id].total_kg_co2e);
  L.STAGES.forEach(st => check(`${p.product_id} ${st}`, s[st], +py1[p.product_id][st]));
});
const options = readCSV("module-2-material-substitution/data/material_options.csv");
const py2 = Object.fromEntries(readCSV("module-2-material-substitution/output/option_comparison.csv").map(r => [r.option_id, r]));
const base = products.find(p => p.product_id === "P01");
options.forEach(o => {
  const p = { ...base, garment_mass_g: o.garment_mass_g, yarn_type: o.yarn_type, washes_in_life: o.washes_in_life, tumble_dry_share_pct: o.tumble_dry_share_pct };
  const s = L.footprint(p, L.parseMaterials(o.materials), legs.filter(l => l.product_id === "P01"), factors.value, G);
  check(`Option ${o.option_id} per garment`, L.total(s), +py2[o.option_id].kg_co2e_per_garment);
});
console.log(failures ? `${failures} differences` : "JavaScript and Python agree.");
process.exit(failures ? 1 : 0);
