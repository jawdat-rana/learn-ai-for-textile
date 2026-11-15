# Module 1 prompts: Product Lifecycle Screening

Copy each prompt into your AI chat in order, in **the same chat**. Text in
`[square brackets]` is for you to change. These are the actual prompts used to
build the code and dashboard in this module.

Works in the free versions of Claude, ChatGPT and Gemini. Free plans have
daily limits, so if you hit one, wait a few hours or switch tools and paste
your earlier results back in.

---

## Prompt 1: Map the life cycle (no data yet)

```text
You are an LCA practitioner who specialises in textiles. I'm a textile
technology manager. I know the processes; I'm new to LCA.

Help me map the full life cycle (cradle to grave) of a 140 g performance
T-shirt: 100% polyester filament yarn, knitted, dyed and finished in China,
sewn in China, shipped by sea to a warehouse in Germany, sold and used in
the EU.

Make one table with a row per stage: fibre, yarn, fabric, dyeing and
finishing, garment making and packaging, transport, use, end of life.
Columns: activities in the stage | data I'd need from suppliers or users |
typical unit (kWh per kg, MJ per kg, tonne-km...) | usually a big or small
share for this kind of product, and why.

Then list what is usually left OUT of a simple screening, and the 3 stages
you'd collect real data for first.

Don't give me any emission factor values. If you're unsure about something,
say so.
```

**Your job:** correct it. For example: *"Disperse dyeing of polyester runs at
about 130 °C under pressure, so heat matters more than you suggest."* You're
the process expert in this chat.

---

## Prompt 2: Understand the data first

*Attach all five files from `data/` before sending.*

```text
I've attached five files for a screening carbon footprint of six made-up
textile products (training data):
products.csv, bill_of_materials.csv, transport_legs.csv,
emission_factors.csv and grid_intensity.csv.

Before any calculation:
1. Explain what each file holds and how they link together (which column
   joins to which), in plain English.
2. Check the data quality: does each product's bill of materials add up to
   100%? Are there transport modes, materials or countries without a factor?
   Any values that look odd?
3. Point out the factors marked Low confidence or ASSUMPTION, and anything
   about the transport that stands out.
4. List 3 questions this data CAN answer and 3 it CANNOT (for example water
   or chemical impacts).

Keep it short and use tables.
```

**What good looks like:** it spots that **P06 adds up to only 85%**, that
**P04 flies** from Vietnam, and that elastane, recycled polyester and the
"biodegradability additive" fibre are low-confidence. It says the data can't
tell you about water, toxicity or microplastics.

---

## Prompt 3: Agree the method and boundary

```text
Propose a simple, transparent screening method using only these files:
- the functional unit
- what's inside and outside the system boundary (be explicit about what we
  leave out and whether that makes our numbers too high or too low)
- how to get from garment weight back to fibre weight (cutting waste and
  the process losses in emission_factors.csv)
- how to calculate each stage, as a formula in words with units
- how to treat biogenic carbon in cotton at end of life
- what to do about P06's missing 15%

Show it as a short table per stage. Then name the 3 weakest assumptions.
Don't calculate anything yet.
```

**Your job:** argue with it. Try: *"Why fill the gap with virgin polyester and
not recycled?"* or *"Our dye house in China uses coal for steam. How does
that change your heat formula?"* Agree the final method before moving on. The
one this course used is in the [module README](README.md#the-method-in-plain-english).

---

## Prompt 4: Have the AI write the code

This is the prompt that produced [analysis/product_lca.py](analysis/product_lca.py).

```text
Write Python code (pandas and matplotlib) that applies the method we agreed
to the attached files. I'll run it in Google Colab and I can't code, so:

- Split it into short numbered steps with a plain-English comment above each.
- If a file isn't found locally, load it from:
  https://raw.githubusercontent.com/[your-github-username]/learn-ai-for-textile/main/module-1-product-lca/data/[file name]
- Step 1: load the five files and turn the factors into a lookup by factor_id.
- Step 2: check the data: bills of materials that don't add up to 100%
  (fill the gap with virgin polyester and print a warning), and any material,
  country or transport mode without a factor.
- Step 3: one function that returns kg CO2e per garment for each of the 8
  stages: raw materials, yarn, fabric, dyeing and finishing, garment making
  (incl. packaging), transport, use, end of life. Never type a factor into
  the code; always read it from the table.
- Step 4: a table of all products by stage, with the total and kg CO2e per kg
  of garment. Save it to output/footprint_by_stage.csv.
- Step 5: a horizontal stacked bar chart, one bar per product, coloured by
  stage. Print each product's biggest stage and its share.
- Step 6: sensitivity for P01: recalculate with each factor at its low and
  high value, one at a time, and draw a tornado chart of the 8 biggest swings.
- Step 7: what-if scenarios, each changing one thing (I'll give you a list).
- Step 8: print a short plain-text summary I can paste back into this chat.

If you can run code, run it and show me the results. If not, tell me exactly
how to run it in Colab.
```

### Prompt 4b: Make it explain the code

```text
Explain this code to me as if I'm a new team member who has never
programmed. For each step: what it does, why it's needed, and one thing I
could change to ask a different question. No jargon, or explain it when you
use it.
```

### Prompt 4c: Check one stage by hand, with units

```text
Walk me through P01 Performance T-shirt by hand for two stages: raw
materials and transport. Show every number with its unit at every step
(g, kg, tonnes, km, tonne-km, kg CO2e) so I can check it on a calculator.
Then tell me the most likely place a units mistake could hide in this code.
```

**What good looks like:** 140 g → 0.140 kg garment → 0.165 kg finished
fabric (15% cutting waste) → about 0.179 kg fibre → × 3.0 = about 0.54 kg
CO2e for raw materials.

### If something breaks

```text
I ran the code and got this error:
[paste the whole red error message]
What does it mean, in plain English, and what exactly should I change?
```

---

## Prompt 5: Hotspots and what to measure first

```text
Using only the code output (don't recalculate anything yourself):
1. For each product, name the biggest stage and explain WHY in one line,
   in terms a textile engineer would recognise.
2. From the sensitivity results, which 3 numbers should we replace with real
   data from our suppliers first, and exactly what should we ask the
   supplier for (with units)?
3. Which results would change most if the Low-confidence factors are wrong?
```

---

## Prompt 6: What-ifs

```text
Add these what-if scenarios to the code, each changing ONE thing, and show
before, after and % change:
- P01 made from 100% recycled polyester
- P01 dyed and finished in Portugal instead of China
- P02 made from organic cotton
- P02 never tumble dried by the customer
- P03 with cutting waste cut from 18% to 10%
- P04 shipped by sea instead of air
- P05 lasting 150 washes instead of 100
Then explain the P05 result: why does a longer-lasting garment have a
HIGHER footprint per garment, and what unit would show the benefit?
```

---

## Prompt 7: Build the dashboard

This is the prompt behind [dashboards/lca-explorer.html](../dashboards/lca-explorer.html).

```text
Create a single HTML file (HTML, CSS and plain JavaScript, no frameworks, no
build step) for GitHub Pages that:
- loads the five CSV files from ../module-1-product-lca/data/ with fetch()
- uses exactly the same method as the Python code, so the numbers match
- shows a stacked bar per product by stage; clicking one selects it
- for the selected product: headline tiles, a bar per stage, and what-if
  controls (main fibre, mill country, sewing country, sea or air, cutting
  waste, washes in life, tumble drying) that show the change vs the original
- shows a "what moves the answer" chart: the total with each factor at its
  low and high value, top 8, low-confidence factors in a different colour
- shows the factors table with sources and confidence
- lets me load my own emission_factors.csv, read only in the browser
- has a "Copy summary for AI" button
- says clearly it is screening level, not an ISO 14040/44 study
- works on a phone and in dark mode
Add short comments in plain English so a non-coder can follow it.
```

If you can, open the result in the AI's preview window. Then add it to your
repository: on GitHub, open the `dashboards` folder, click **Add file →
Create new file**, name it, paste the code and commit.

---

## Prompt 8: The internal screening summary

Example result: [output/screening_summary.md](output/screening_summary.md).

```text
Write a one-page internal summary for our Head of Product and Head of
Sustainability:
- a 3-line headline: what we found and what we recommend
- a short table of products, total kg CO2e and the main hotspot
- the 3 levers worth testing first, with the what-if result for each
- the data we must collect from suppliers next, and from whom
- a "Limits of this screening" box: not ISO 14040/44, climate only, what's
  outside the boundary, and that these numbers must NOT be used in
  marketing or on labels
Plain business English, under 350 words. Use only numbers from the code
output; round to 1 decimal place.
```

---

## Prompt 9: The consultant brief

Example result: [output/consultant_brief.md](output/consultant_brief.md).
There is also a reusable [prompt kit](../prompt-kits/lca-scope-and-consultant-brief.md).

```text
We may commission an external ISO 14040/44 LCA for [P01 Performance
T-shirt]. Using what we've learned, draft a request for quotation brief:
- goal of the study and intended audience (internal only, or a public
  comparative claim, which needs a critical review panel)
- functional unit and system boundary we propose
- impact categories (climate plus which others, and why)
- the hotspots our screening found, and the primary data we can supply
- what we want back (report, model files, data quality assessment)
- 8 questions to ask every consultant so quotes are comparable
Under 2 pages. Mark anything I need to decide with [DECISION].
```

---

## Bonus: challenge the AI

```text
Play the critical reviewer of this study. Give me the 5 strongest reasons
these results could be wrong or misleading, how big each effect could be,
and what data would fix it.
```
