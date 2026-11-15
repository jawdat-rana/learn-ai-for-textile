# Module 2: Material Substitution Explorer

> **The question:** "If we change the fibre in our performance T-shirt, is it
> really better, by how much, and how sure can we be?"

Product teams ask this every season: recycled polyester, organic cotton, a
blend, a new "biodegradable" polyester. You will reuse the Module 1 model to
compare six fibre options for the same T-shirt, per garment **and per wear**,
with uncertainty ranges. Then you'll weigh the things a carbon number can't
show (microplastics, water, end of life, cost) and write a recommendation
that doesn't over-claim.

**Time:** 90 minutes · **Do Module 1 first** · **Data:** made-up options and
costs, public emission factors with [sources](../SOURCES.md)

| What you get at the end | Where it lives |
|---|---|
| kg CO2e per garment and g CO2e per wear for six options, with ranges | Your AI chat, and [the live dashboard](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/materials.html) |
| A weighted scorecard you can re-weight live | The dashboard |
| A recommendation for the product team, including what NOT to claim | [output/recommendation.md](output/recommendation.md) (example) |
| A list of evidence to request from the "biodegradable" fibre supplier | Your AI chat |

---

## The files

| File | What it is |
|---|---|
| [data/material_options.csv](data/material_options.csv) | Six options: fibres, garment weight, yarn type, assumed washes in life, tumble drying, made-up fibre cost |
| [data/beyond_carbon.csv](data/beyond_carbon.csv) | Judgement scores (1 to 5, 5 = best) for microplastics, water, end of life and quality of evidence, each with a one-line reason |
| Module 1's [data/](../module-1-product-lca/data/) | Emission factors, grid factors and the base T-shirt (P01) |
| [prompts.md](prompts.md) | Every prompt used in this module |
| [analysis/material_compare.py](analysis/material_compare.py) | The Python the AI wrote. [Open it in Google Colab](https://colab.research.google.com/github/jawdat-rana/learn-ai-for-textile/blob/main/module-2-material-substitution/analysis/material_compare.ipynb) |
| [../dashboards/materials.html](../dashboards/materials.html) | The interactive comparison ([see it live](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/materials.html)) |

---

## The steps

Prompts are in [prompts.md](prompts.md). One chat for the whole module.

### Step 1: Agree what "better" means before any numbers (10 min)

Use **Prompt 1**. The AI should ask *better per what?* One T-shirt? One
kilogram? One wear? A cotton T-shirt is heavier and, in this example, lasts
fewer washes, so the unit decides the winner. Agree on **per wear** as the
main unit, with per garment shown too.

### Step 2: Check the options (10 min)

Upload the two files and use **Prompt 2**. The AI should notice that
**washes in life is an assumption**, that cotton options are heavier, and
that option E is a **generic placeholder** with no supplier data at all.

### Step 3: Have the AI write and run the comparison (20 min)

Use **Prompt 3**, the prompt behind
[analysis/material_compare.py](analysis/material_compare.py). Run it in the
chat or [in Colab](https://colab.research.google.com/github/jawdat-rana/learn-ai-for-textile/blob/main/module-2-material-substitution/analysis/material_compare.ipynb).
It calculates every option with the Module 1 model, then again with the
fibre and landfill factors at their low and high values to get a range.

### Step 4: Read the ranges, not just the bars (10 min)

Use **Prompt 4**. Where two options' ranges overlap, this data **cannot**
tell you which is better. Saying so is the honest, professional answer.

### Step 5: Test durability (10 min)

Use **Prompt 5**, or type new numbers in the "washes in life" column of the
dashboard. How many washes would organic cotton need to match virgin
polyester per wear? Durability is a design lever, not just a fibre choice.

### Step 6: Beyond carbon, and the biodegradability question (15 min)

Use **Prompt 6** to build the weighted scorecard, then **Prompt 6b** to
list the evidence you'd ask a supplier for before believing a
"biodegradable polyester" claim (which test standards, which conditions,
how long, what residue). In the dashboard, tick "Accept option E's claim"
and see how much the ranking depends on an unproven claim.

### Step 7: Write the recommendation (15 min)

Use **Prompt 7**. Example result:
[output/recommendation.md](output/recommendation.md).

---

## Check your answers

For the performance T-shirt (P01 settings, China, sea to the EU):

| Option | kg CO2e per garment | Washes | g CO2e per wear (range) |
|---|---|---|---|
| B. Recycled polyester | 2.15 | 50 | 43 (41-45) |
| A. Virgin polyester | 2.43 | 50 | 49 (46-58) |
| E. Polyester with biodegradability additive (generic) | 2.45 | 50 | 49 (46-59) |
| F. Recycled polyester and organic cotton 50/50 | 2.63 | 45 | 58 (56-61) |
| D. Organic cotton | 2.87 | 40 | 72 (68-75) |
| C. Conventional cotton | 3.17 | 40 | 79 (65-92) |

- **4 of 15 pairs overlap**, including virgin polyester vs option E and
  organic vs conventional cotton. This data can't separate them.
- With the default weights the scorecard ranks recycled polyester first
  (3.90) and conventional cotton last (2.09). Set microplastics to 50,
  climate to 20, end of life to 10, and water and cost to 0, and organic
  cotton comes first (3.33). The weights decide the winner.
- Organic cotton needs about **67 washes** (instead of 40) to match virgin
  polyester per wear; conventional cotton about 76.

---

## Where AI is wrong (read this before using it at work)

1. **"Polyester is better than cotton."** Per garment, per kg and per wear
   can give different answers. If the AI declares a winner without saying
   per what, stop it.
2. **Overlapping ranges ignored.** The AI will happily rank options 0.1 kg
   apart. Ask: "Do the ranges overlap? Then what can we honestly say?"
3. **Recycled = always better.** Recycled polyester's benefit depends on
   the allocation method and electricity used, and it still sheds microfibres.
   Also, bottle-to-fibre recycling takes bottles out of the bottle loop.
4. **Believing "biodegradable".** An AI will repeat marketing language as
   fact. Biodegradation depends on the environment (industrial compost, soil,
   seawater, landfill), temperature and time, and must be shown with test
   reports. In landfill, a material that really degrades can make methane.
5. **Relative scores look absolute.** In the scorecard, the best option gets
   5 and the worst 1 even if they're nearly identical. A 4.4 vs 5.0 on
   climate here is a 6 g per wear difference.
6. **Weights hide opinions.** Whoever sets the weights picks the winner.
   Show the weights, and show what changes when they move.
7. **Invented cost and durability data.** Ask the AI for typical prices or
   wash life and it may make them up. Use your own lab and buying data.

## Taking this to work

- Replace the made-up washes with your **own durability test results** (for
  example pilling and dimensional stability after N washes) and your own
  wear data.
- Ask fibre suppliers for **product-specific cradle-to-gate footprints**
  (with the method, database and allocation stated), and for test reports
  behind any biodegradability or microfibre claim. The
  [lab report kit](../prompt-kits/lab-report-to-plain-english.md) helps
  you read them.
- Before anything goes in marketing, run the
  [green claims check](../prompt-kits/green-claims-check.md) and talk to
  your legal team.
