# Module 1: Product Lifecycle Screening

> **The question:** "Across its whole life, where does our product's climate
> impact come from, and what would it be worth changing first?"

You will use a free AI chat tool to map a garment's life cycle, check the
data, build a simple cradle-to-grave carbon model, find the hotspots, test
what-ifs and write two documents: an internal summary and a brief for an
external LCA consultant. You will not write any code yourself. The AI writes
it, explains it and runs it (or you run it in Google Colab with one click).

**Time:** 90 to 120 minutes · **You need:** a free account on Claude, ChatGPT
or Gemini · **Data:** made-up products, public emission factors with
[sources](../SOURCES.md)

> **Screening level, not an ISO 14040/44 study.** This gives you a reliable
> picture of *where* the impact is and *what moves it*. It does not give you a
> number you can print on a label. Module 1 ends with the brief you'd send a
> consultant if you need that.

| What you get at the end | Where it lives |
|---|---|
| kg CO2e per garment for six products, split into eight life cycle stages | Your AI chat, and [the live dashboard](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/lca-explorer.html) |
| A hotspot chart and a "what moves the answer" sensitivity chart | [output/](output/) and the dashboard |
| Seven what-if scenarios (recycled fibre, a different dye house, sea instead of air...) | Your AI chat and the dashboard |
| An internal screening summary | [output/screening_summary.md](output/screening_summary.md) (example) |
| A brief for an LCA consultant | [output/consultant_brief.md](output/consultant_brief.md) (example) |

---

## The files

| File | What it is |
|---|---|
| [data/products.csv](data/products.csv) | Six made-up products: weight, yarn type, knit or woven, where it's made, cutting waste, washes in its life, tumble drying, end-of-life split |
| [data/bill_of_materials.csv](data/bill_of_materials.csv) | Fibre content of each product. **One of them doesn't add up** |
| [data/transport_legs.csv](data/transport_legs.csv) | Each transport leg: what's carried, mode and distance |
| [data/emission_factors.csv](data/emission_factors.csv) | 39 factors with value, low-high range, confidence and source code |
| [data/grid_intensity.csv](data/grid_intensity.csv) | kg CO2e per kWh of grid electricity by country (2024) and the main boiler fuel |
| [data/README.md](data/README.md) | What every column means |
| [prompts.md](prompts.md) | **Every prompt used in this module, in order.** Copy and paste them |
| [analysis/product_lca.py](analysis/product_lca.py) | The Python the AI wrote in Step 4 |
| [analysis/product_lca.ipynb](analysis/product_lca.ipynb) | The same code as a notebook. [Open it in Google Colab](https://colab.research.google.com/github/jawdat-rana/learn-ai-for-textile/blob/main/module-1-product-lca/analysis/product_lca.ipynb) |
| [../dashboards/lca-explorer.html](../dashboards/lca-explorer.html) | The interactive dashboard the AI built in Step 7 ([see it live](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/lca-explorer.html)) |

---

## The steps

Each step has a ready-made prompt in [prompts.md](prompts.md). Keep everything
in **one chat** so the AI remembers what came before.

### Step 1: Map the life cycle with the AI as your coach (10 min)

Before any data, use **Prompt 1** to have the AI map the life cycle of a
polyester T-shirt with you: stages, activities, data needed, units. You know
the textile process far better than the AI. Correct it where it's vague
("dyeing" for polyester means disperse dyes at around 130 °C, so heat
matters).

### Step 2: Ask the AI to understand the data before it calculates (15 min)

Upload the five CSV files and use **Prompt 2**. A good answer explains each
file and spots the problems. **It should notice that P06 Swim shorts' fibres
add up to only 85%** (the lining is missing), that P04 Sports leggings fly by
air, and that some factors are marked "Low" confidence or "ASSUMPTION". If it
misses any, ask.

### Step 3: Agree the method and the boundary (15 min)

Use **Prompt 3**. The AI proposes the functional unit, what's in and out of
the system boundary, and how to handle the gaps. Push back. The method this
course settled on is below.

### Step 4: Have the AI write the code and run it (20 min)

Use **Prompt 4**. You described the method in plain English and the AI
writes a program for it. Then:

- **If your AI can run code**, let it run and show you the results.
- **If it can't**, open the notebook in
  [Google Colab](https://colab.research.google.com/github/jawdat-rana/learn-ai-for-textile/blob/main/module-1-product-lca/analysis/product_lca.ipynb)
  and press **Runtime → Run all**. Nothing to install.

Then use **Prompt 4b** to have the AI explain the code like you're a new team
member, and **Prompt 4c** to walk through one stage by hand with units at
every step. This is how you check code you can't read.

### Step 5: Find the hotspots and what moves the answer (15 min)

Use **Prompt 5**. The AI ranks stages for each product and runs a
**sensitivity check**: each factor at the low and high end of its published
range. The biggest swings are where you should collect real supplier data
first. That list is worth more than the footprint number itself.

### Step 6: Test what-ifs (15 min)

Use **Prompt 6** to test changes one at a time: recycled polyester, a dye
house in Portugal, sea instead of air, less cutting waste, a longer life.
Then try your own in the [dashboard](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/lca-explorer.html).

### Step 7: Build the dashboard, the summary and the consultant brief (20 min)

Use **Prompt 7** for the dashboard, **Prompt 8** for a one-page internal
summary and **Prompt 9** for a brief you'd send an LCA consultant. A clear
brief, with the hotspots already known, gets you faster, cheaper and more
comparable quotes.

---

## The method, in plain English

- **Functional unit:** one garment, used for its expected life, in the EU.
  Module 2 adds "per wear".
- **Boundary:** cradle to grave. In: fibre, yarn, fabric, dyeing and
  finishing, garment making and packaging, transport, washing and drying,
  end of life. **Out:** chemicals and dyes themselves, water treatment,
  detergent, ironing, retail, the buildings and machines, and upstream
  emissions of producing the fuels (this makes our numbers a little low).
- **Work backwards from the garment:** cutting waste (12-20%), finishing
  losses (3%), knitting or weaving losses (2%) and spinning losses (3% for
  filament, 10% for staple) mean a 140 g T-shirt needs about 179 g of fibre.
- **Factory energy:** kWh × the grid factor of the mill's country. Heat for
  dyeing: MJ ÷ boiler efficiency × the fuel factor (coal in China, India and
  Vietnam; gas elsewhere, as a simplification).
- **Transport:** (kg ÷ 1,000) × km × factor per tonne-km. Fibre legs carry
  the fibre weight, later legs carry the garment plus packaging.
- **Use:** washes × (garment weight ÷ 3.5 kg load) × (washing kWh + tumble
  dry share × dryer kWh) × EU grid factor.
- **End of life:** 40% burned, 30% landfilled, 30% reused or recycled
  (counted as zero here). Burning synthetics releases fossil CO2 (2.29 kg per
  kg of polyester, from its carbon content). Cotton's carbon is biogenic and
  counts as zero when burned, but cotton in landfill makes some methane.
- **Gaps:** a bill of materials that doesn't add up to 100% is filled with
  virgin polyester (a cautious choice) and flagged.

---

## Check your answers

If your numbers differ, that's fine as long as you can explain why. With the
method above you should see (kg CO2e per garment):

| Product | Total | Biggest stage |
|---|---|---|
| P01 Performance T-shirt | 2.43 | Dyeing and finishing (29%) |
| P02 Classic cotton T-shirt | 3.13 | Yarn (25%) |
| P03 Fleece jacket | 6.64 | Dyeing and finishing (33%) |
| P04 Sports leggings | 7.89 | Transport (34%), because it flies |
| P05 Workwear trousers | 12.82 | Use (42%): 100 washes, half tumble dried |
| P06 Swim shorts | 1.72 | Dyeing and finishing (28%) |

- **Data problem:** P06's fibres add up to 85%; the gap is filled with virgin
  polyester and flagged.
- **Biggest swing for P01:** dyeing heat (2.09 to 3.00 kg CO2e), then the
  polyester fibre factor (2.29 to 2.88). So the dye house's real gas or coal
  use is the first number to ask for.
- **What-ifs:** sea instead of air cuts P04 by 33%. Dyeing in Portugal instead
  of China cuts P01 by 27%. Recycled polyester cuts P01 by 12%. Organic
  cotton cuts P02 by 10%.

---

## Where AI is wrong (read this before using it at work)

These are real failure patterns. Watch for each one in your own chat.

1. **Invented emission factors with real-sounding citations.** Ask "what's
   the factor for polyester?" and you may get "3.42 kg CO2e/kg (Higg MSI
   2023)" that nobody can find. Only use factors from a table you control,
   and check every citation.
2. **Unit slips.** Grams vs kilograms, and kilograms vs tonnes in tonne-km,
   are the classic bugs. A 1,000× error looks fine in a long table. Prompt 4c
   exists for this.
3. **Double counting.** Counting spinning energy in both "fibre" and "yarn",
   or the garment weight on every transport leg including the fibre ones.
   Ask "is any activity counted twice?"
4. **Biogenic carbon done wrong.** Some AIs count CO2 from burning cotton, or
   give cotton a big "carbon storage" credit. Ask how it treated it.
5. **Missing data quietly filled in.** The AI may scale P06 to 100% without
   telling you. Always ask "how did you handle the 85%?"
6. **False precision and false certainty.** "2.4316 kg" and "polyester is
   better than cotton" both sound authoritative. Round, show ranges, and see
   Module 2 for why per-garment comparisons mislead.
7. **Turning screening into claims.** Ask for a summary and the AI may write
   "our T-shirt has a low carbon footprint of 2.4 kg". That's a public claim
   from a screening model. Don't.
8. **It agrees with you too easily.** Ask "what would make this ranking
   wrong?" A good LCA practitioner answers that question; make the AI do it.

## Taking this to work

- Use only the AI tools your company has approved, and follow its data
  policy. Bills of materials, recipes and supplier energy data are
  confidential.
- If you can't upload real data, **anonymise** it: product codes instead of
  names, rounded weights. The method works the same.
- The [dashboard](https://jawdat-rana.github.io/learn-ai-for-textile/dashboards/lca-explorer.html)
  lets you load your own factors file. It's read on your computer and nothing
  is uploaded.
- Replace the biggest-swing factors with **primary data** from your mills
  first: kWh and gas or coal per kg of fabric at the dye house, spinning
  energy, cutting waste. Then decide which products need a full study.
