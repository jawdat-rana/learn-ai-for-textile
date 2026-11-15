# Module 1 data dictionary

All products, companies and suppliers are **made up**. Emission factors are
public, rounded values; see [SOURCES.md](../../SOURCES.md) for every source
and how far to trust it.

## products.csv (one row per product)

| Column | Meaning |
|---|---|
| `product_id`, `product_name` | Made-up product |
| `yarn_type` | `filament` (extruded, for example polyester and nylon) or `staple` (spun from short fibres, for example cotton and blends) |
| `construction` | `knit` or `woven` |
| `garment_mass_g` | Finished garment weight in grams |
| `mill_country` | Where yarn, fabric, dyeing and finishing happen (one country, to keep it simple) |
| `make_country` | Where the garment is cut and sewn |
| `market` | Where it is used; sets the electricity factor for washing (`EU-27`) |
| `cut_waste_pct` | Fabric lost when cutting the pattern pieces |
| `washes_in_life` | Expected number of washes before it's thrown away |
| `tumble_dry_share_pct` | Share of washes followed by tumble drying |
| `incineration_pct`, `landfill_pct` | End-of-life split. The rest is reused or recycled and counted as zero (cut-off approach) |

## bill_of_materials.csv (one row per fibre per product)

| Column | Meaning |
|---|---|
| `component` | Part of the garment |
| `material` | A `factor_id` from emission_factors.csv, for example `FIB_PES` |
| `share_pct` | Share of the garment's weight. Should add up to 100 per product. **P06 doesn't**: its polyester mesh lining is missing |

## transport_legs.csv (one row per leg)

| Column | Meaning |
|---|---|
| `leg` | Description |
| `cargo` | `fibre` (carries the fibre weight) or `garment` (carries the garment plus 40 g of packaging) |
| `mode` | `truck`, `sea`, `rail` or `air`, matching factors `TR_TRUCK`, `TR_SEA` and so on |
| `distance_km` | Distance in km |

## emission_factors.csv (one row per factor)

| Column | Meaning |
|---|---|
| `factor_id` | Short code used by the code and the bill of materials |
| `stage`, `item` | Where and what |
| `value` | The value used in the base case |
| `unit` | Always read this. kWh per kg, MJ per kg and kg CO2e per tonne-km are easy to mix up |
| `low`, `high` | Published range, used for the sensitivity check |
| `confidence` | High, Medium or Low: how well the value is supported |
| `source` | Code in SOURCES.md, or ASSUMPTION |
| `notes` | Why the value is what it is |

## grid_intensity.csv (one row per country)

| Column | Meaning |
|---|---|
| `kg_co2e_per_kwh` | Grid electricity, 2024 (Ember via Our World in Data) |
| `heat_fuel` | Main boiler fuel assumed for dyeing heat in that country: `coal` or `gas`. A simplification: ask your dye house what it really burns |
