# Module 2 prompts: Material Substitution Explorer

Use **one chat** for the whole module. If you can, continue in the same chat
as Module 1 so the AI already knows the model. Text in `[square brackets]` is
for you to change.

---

## Prompt 1: What does "better" mean?

```text
You are an LCA practitioner who specialises in textile materials. Our
product team wants to replace the fibre in our 140 g performance T-shirt
(currently 100% virgin polyester). Options: recycled polyester, conventional
cotton, organic cotton, a polyester with a biodegradability additive, and a
recycled polyester / organic cotton blend.

Before any numbers: what should we compare them on? Explain the choice of
functional unit (per garment, per kg, per wear) and show with a simple
made-up example how each can give a different winner. Then list what a
carbon footprint can't tell us about these options.
```

**What good looks like:** it argues for **per wear** (or per year of use) as
the main unit, and mentions microplastics, water scarcity, chemicals, land
use and recyclability as things carbon misses.

---

## Prompt 2: Check the options

*Attach `data/material_options.csv` and `data/beyond_carbon.csv`.*

```text
Here are the six options (made-up training data) and a table of judgement
scores. Check them before we calculate:
1. Which numbers are measured facts and which are assumptions?
2. Is anything inconsistent (weights, yarn types, washes)?
3. For each beyond-carbon score, do you agree with the reason given? Where
   would an expert challenge it?
4. What evidence would we need for option E?
```

**What good looks like:** it says washes in life and fibre costs are
assumptions, notices the cotton options are heavier and staple-spun, and
says option E has no data behind it at all.

---

## Prompt 3: Have the AI write and run the comparison

This is the prompt behind [analysis/material_compare.py](analysis/material_compare.py).

```text
Write Python code (pandas and matplotlib) for Google Colab, for a non-coder,
in short numbered steps with plain-English comments:
- Load Module 1's emission_factors.csv, grid_intensity.csv, products.csv
  and transport_legs.csv, plus material_options.csv and beyond_carbon.csv,
  from https://raw.githubusercontent.com/[your-github-username]/learn-ai-for-textile/main/
  if they aren't found locally.
- Reuse the Module 1 footprint function UNCHANGED. Each option is product
  P01 with the option's fibres, weight, yarn type, washes and tumble drying.
- For each option: kg CO2e per garment, g CO2e per wear (one wear per wash,
  as a setting I can change), and a low-high range with the option's fibre
  and landfill factors at their low and high values.
- A bar chart of g CO2e per wear with the ranges as error bars, and a list
  of option pairs whose ranges overlap.
- A weighted scorecard (5 = best): climate per wear and fibre cost scaled
  from best to worst, plus the judgement scores. Weights as a dictionary I
  can edit. A setting to accept option E's biodegradability claim (score 4
  for microplastics instead of 1). Keep the evidence score OUT of the total
  but show it.
- Save the comparison and scorecard to output/ and print a summary I can
  paste back into this chat.
Run it if you can.
```

---

## Prompt 4: Read the ranges

```text
Using only the code output: which options can this data honestly separate
on climate, and which can't? Write it as three sentences a product director
would understand, without the word "statistically".
```

---

## Prompt 5: Durability

```text
Change washes in life for organic cotton until its g CO2e per wear matches
virgin polyester. How many washes is that? Then tell me what lab tests and
wear trials would tell us whether that's realistic, and what design changes
(fabric weight, construction, finishing) could make a garment last longer.
```

---

## Prompt 6: Beyond carbon

```text
Explain the scorecard to me. Then:
1. Show how the top 3 change if microplastics is weighted 50% instead of 20%.
2. Show how much option E's position depends on accepting its claim.
3. Which single score, if wrong, would change the recommendation?
```

### Prompt 6b: The evidence list for a "biodegradable polyester"

```text
A supplier says their polyester with an additive is "biodegradable" and
"ocean safe". Write the list of evidence I should ask for before believing
it: which test standards are relevant for which environments (industrial
compost, soil, freshwater, seawater, landfill), what conditions and duration,
what pass criteria, what residue and ecotoxicity tests, whether the fabric
still recycles with normal polyester, and who ran the tests. Then list the
red flags in a test report. If you're not sure a standard number is right,
say so and tell me to check it.
```

**Your job:** check every standard number the AI gives you on the standards
body's website. AIs often get these slightly wrong.

---

## Prompt 7: The recommendation

Example result: [output/recommendation.md](output/recommendation.md).

```text
Write a half-page recommendation for our product team:
- which option to test first and why, using per-wear results and ranges
- what we can and can't conclude, honestly
- the evidence we need from suppliers before deciding
- a "do not claim" box: statements marketing must not make from this
  screening (with a one-line reason each)
Under 300 words, numbers only from the code output.
```
