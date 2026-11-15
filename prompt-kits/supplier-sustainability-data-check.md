# Kit 1: Supplier sustainability data check

**Use it when:** your suppliers have answered a sustainability or LCA data
questionnaire and you need to know what's usable, what's missing and what to
ask next, before it goes into a footprint.

**Try it with:** [samples/supplier-responses.md](samples/supplier-responses.md),
answers from three made-up mills with typical problems.

> Real supplier answers are confidential. Anonymise them (Mill A, Mill B),
> and use only AI tools your company allows.

## The prompt

```text
You are an LCA data analyst for a textile brand. Below are suppliers'
answers to our data request. For an LCA we need, per kg of output: electricity
(kWh), heat (MJ) and the fuel used to make it, the reporting period, whether
figures are measured or estimated, and the share of renewable electricity
with proof (certificates or contracts).

For each supplier, produce:
1. A table: data item | value as given | unit as given | converted to our
   unit (show the conversion) | measured or estimated | usable? (yes / with
   caveat / no) | why.
2. Inconsistencies and red flags: units that don't make sense, numbers far
   outside typical ranges, mixed reporting periods, claims without evidence.
3. A polite follow-up email to each supplier asking only for what's missing,
   with the exact units we want.

Never fill a gap with your own estimate. If something is unclear, write
"ASK SUPPLIER".

[paste supplier answers]
```

## What good looks like (for the sample)

It should notice that **Mill A** reports energy **per metre, not per kg**
(it needs the fabric weight in g per square metre and width to convert);
**Mill B** gives annual totals for the whole site, not per kg, and mixes 2024
electricity with 2025 production; and **Mill C** claims "100% renewable
energy" while also listing a coal boiler, with no certificates. A good answer
converts only what can be converted, and shows the maths.

## Where AI is wrong

- **It converts units confidently and wrongly.** Per metre to per kg needs
  the fabric weight; MJ, kWh and therms are easy to mix up. Check one
  conversion by hand.
- **It fills gaps "helpfully".** If it writes a number the supplier never
  gave, stop it. That's how made-up data ends up in a footprint.
- **It believes claims.** "100% renewable" without certificates, or
  "carbon neutral" through offsets, aren't the same as low-carbon energy
  use. Ask for proof.
- **It doesn't know your suppliers.** A number that looks odd may be right
  (a mill with heat recovery). Use the AI's flags as questions, not verdicts.

## Make it yours

Paste your real questionnaire into the prompt so the AI checks answers
against your exact questions and units.
