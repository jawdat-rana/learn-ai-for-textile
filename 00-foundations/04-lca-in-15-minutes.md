# 4. LCA in 15 minutes

A **lifecycle analysis (LCA)** adds up the environmental impact of a product
across its whole life. This course focuses on one impact, **climate change,
measured in kg CO2e** (kilograms of CO2 equivalent: all greenhouse gases
converted to the warming effect of CO2). A full LCA also covers water,
toxicity, land use and more.

## The life of a garment

```text
Fibre  →  Yarn  →  Fabric  →  Dyeing and   →  Garment  →  Transport  →  Use        →  End of life
(farm or  (spin    (knit or    finishing       making      (truck, ship,  (washing,     (burned,
 polymer)  or       weave)     (heat, water,   (cut, sew,   air)           drying)       landfilled,
           extrude)            chemicals)       pack)                                    reused)
```

"Cradle to gate" stops when the product leaves the factory. "Cradle to grave"
(this course) goes all the way to disposal.

## Six words you need

| Word | Plain English | Example from this course |
|---|---|---|
| **Functional unit** | What exactly you're measuring the impact *of*. It must be the same when you compare things. | "One T-shirt" vs "one wear of a T-shirt". A shirt that lasts twice as long can win per wear and lose per garment. |
| **System boundary** | Which stages and activities you include, and which you leave out. Always write down what's out. | We leave out detergent, ironing, retail stores and the factory buildings. |
| **Activity data** | How much of something happens. | 0.18 kg of fibre for one T-shirt; 5 kWh to spin 1 kg of yarn; 19,500 km by ship. |
| **Emission factor** | kg CO2e per unit of activity. | 0.555 kg CO2e per kWh of Chinese grid electricity; 0.016 kg CO2e per tonne-km by container ship. |
| **Hotspot** | The stage or input that contributes most. | Dyeing and finishing for polyester; air freight for the leggings. |
| **Sensitivity** | How much the answer moves if an input changes. | If the elastane factor is 10 instead of 20, the leggings move by about 0.65 kg CO2e (8%). |

**The whole method in one line:** footprint = Σ (activity data × emission
factor), for every activity inside the boundary.

## Primary vs secondary data

- **Primary data** comes from your own supply chain: your dye house's
  actual gas bill per kg of fabric. Best, but takes effort to collect.
- **Secondary data** comes from databases and studies: an average for
  "polyester dyeing". Fast, but can be far from your reality.

A good in-house LCA starts with secondary data, finds the hotspots, then
collects primary data **only where it matters**. That's exactly what
Module 1 teaches.

## Screening LCA vs a certified study

| | Screening (this course) | ISO 14040/44 study |
|---|---|---|
| Purpose | Internal: find hotspots, compare options, prioritise | Internal and external decisions, public claims |
| Data | Mostly secondary, rounded public factors | Primary data for key processes plus licensed databases (ecoinvent, Sphera, Higg MSI) |
| Impacts | Usually climate only | Several impact categories |
| Review | You and a colleague | Comparative public claims need a critical review panel |
| Cost and time | Days, nearly free | Weeks to months; consultancy fees |
| Can I put it on a label? | **No** | Yes, if done to the right rules |

In the EU, the **Product Environmental Footprint (PEF)** method and its
category rules for apparel are becoming the reference. And since September
2026 the EU restricts vague claims like "eco-friendly" (see
[SOURCES.md](../SOURCES.md)). Screening results are for steering your work,
not for marketing.

## Five traps that catch everyone

1. **Comparing with different functional units.** Per garment vs per kg vs
   per wear give different winners.
2. **Biogenic carbon.** Cotton's carbon came from the air. By convention, CO2
   from burning cotton counts as zero, but methane from cotton rotting in
   landfill does count.
3. **Persistence isn't climate.** Polyester barely changes the climate
   number at end of life in landfill, but microfibres persist for decades.
   A carbon footprint can't see that, so Module 2 adds other criteria.
4. **"Biodegradable" can raise the climate number.** If a material really
   degrades in a landfill without oxygen, it can make methane. Whether that
   happens, and how fast, is a question for test data, not for marketing.
5. **False precision.** "2.4316 kg CO2e" means nothing when the factors have
   ±50% ranges. Round, show ranges, and say what you left out.

**Next:** [Module 1: Product Lifecycle Screening](../module-1-product-lca/README.md)
