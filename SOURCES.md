# Sources and how far to trust them

Every number in `module-1-product-lca/data/emission_factors.csv` has a source
code (S1 to S14) or the word **ASSUMPTION**. This page explains each code.

> **Be honest about what this is.** The factors are rounded, mid-range values
> picked to teach the method. They are good enough to find hotspots and
> compare options roughly (a *screening* LCA). They are **not** good enough
> for a label, a website claim, a customer tender or a comparison you publish.
> For that you need primary data from your suppliers, a licensed database such
> as ecoinvent or the Higg Materials Sustainability Index, and an ISO 14040/44
> study with critical review (or a PEF study under the EU method).

The "Checked" column says whether the number was looked up while this course
was being built (November 2026) or comes from well-known literature that you
should check yourself before relying on it.

| Code | Source | Used for | Checked |
|---|---|---|---|
| S1 | PlasticsEurope, *Eco-profiles* of plastics (PET, nylon 6, LDPE). [plasticseurope.org](https://plasticseurope.org/sustainability/circularity/life-cycle-thinking/eco-profiles-set/) | Polymer production before fibre making; polybag | Literature, verify the current version |
| S2 | Kirchain, Olivetti, Miller and Greene (2015), *Sustainable Apparel Materials*, MIT Materials Systems Laboratory | Ranges for synthetic fibres | Literature, verify |
| S3 | Textile Exchange (June 2026), *Life Cycle Assessment for Polyester: Summary*. [PDF](https://textileexchange.org/app/uploads/2026/06/Polyester-LCA_Summary.pdf) | Virgin vs recycled polyester. The public summary has **no numbers**; the values sit in the full report | Summary read; numbers not in it |
| S4 | Organic Cotton Accelerator and South Pole, India study (about 18,000 farms, field to ginning gate), as reported by Carbonfact, *The carbon footprint of cotton* (updated July 2026). [carbonfact.com](https://www.carbonfact.com/blog/knowledge/carbon-footprint-cotton) | Conventional irrigated cotton about 2.70, organic rain-fed about 1.53 kg CO2e per kg lint | Checked (secondary source) |
| S5 | Textile Exchange cotton LCA (March 2026), values as reported by Carbonfact (link above). Organic: Turkey 0.95, India 1.46, US 1.77 kg CO2e per kg. Textile Exchange says not to compare countries directly | Organic cotton range | Checked (secondary source) |
| S6 | van der Velden, Patel and Vogtländer (2014), "LCA benchmarking study on textiles made of cotton, polyester, nylon, acryl, or elastane", *International Journal of Life Cycle Assessment* 19, 331-356 | Spinning, knitting, weaving energy; process losses | Literature, verify |
| S7 | Sandin, Roos, Spak, Zamani and Peters (2019), *Environmental assessment of Swedish clothing consumption: six garments, sustainable futures*, Mistra Future Fashion report 2019:05 | Process energy ranges; garment making; finishing losses | Literature, verify |
| S8 | Quantis (2018), *Measuring Fashion: environmental impact of the global apparel and footwear industries* | Dyeing and finishing as a major hotspot | Literature, verify |
| S9 | IPCC (2006), *Guidelines for National Greenhouse Gas Inventories*: Vol. 2 ch. 2 (default fuel emission factors: natural gas 56,100 and bituminous coal 94,600 kg CO2 per TJ) and Vol. 5 (waste) | Boiler fuels; landfill methane logic | Standard defaults |
| S10 | UK Government (DESNZ/Defra), *Greenhouse gas reporting: conversion factors*, material use and waste disposal tabs. [gov.uk](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting) | Cardboard; landfill | Literature, verify the current year |
| S11 | UK Government (DESNZ/Defra) conversion factors, freighting goods tab (link above), and Smart Freight Centre, *GLEC Framework* (aligned with ISO 14083) | Truck, ship, rail and air freight per tonne-km | Rounded; verify the current year |
| S12 | EU energy labelling and ecodesign rules for household washing machines (Regulations (EU) 2019/2014 and 2019/2023) and tumble dryers (Regulation (EU) 392/2012) | Energy per wash and per dryer load | Typical label values, verify |
| S13 | Chemistry: the carbon share of each polymer times 44/12 (the mass of CO2 per unit of carbon) | Fossil CO2 when synthetics are burned | Calculated |
| S14 | Ember, via Our World in Data, *energy-data* (column `carbon_intensity_elec`, year 2024). [github.com/owid/energy-data](https://github.com/owid/energy-data) | Grid electricity by country | Checked (downloaded Nov 2026) |
| ASSUMPTION | Made up by the course as a reasonable placeholder | Laundry load, packaging weights, boiler efficiency, the generic "biodegradability additive" fibre | Replace with your own data |

## Standards and rules worth knowing (not used for numbers)

- **ISO 14040 and ISO 14044** (2006): the international standards for LCA.
  Comparative claims made public need a critical review panel.
- **ISO 14067** (2018): carbon footprint of products.
- **GHG Protocol Product Life Cycle Standard**.
- **EU Product Environmental Footprint (PEF)** and the draft category rules
  for apparel and footwear (PEFCR).
- **Directive (EU) 2024/825** on empowering consumers for the green
  transition: from 27 September 2026 it bans generic environmental claims
  ("eco-friendly", "green") without recognised excellent performance, and
  claims based on offsetting. Check with your legal team for your market.

Rules change often. Ask the AI to summarise a rule only after you paste the
official text, and always check the date.
