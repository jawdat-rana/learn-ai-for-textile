# 2. Prompting for technical leaders

You already know how to brief a capable new analyst. A good prompt is the same
thing written down.

## The briefing pattern: R-C-T-F-C

| Part | Question it answers | Example |
|---|---|---|
| **Role** | Who should the AI be? | "You are an LCA practitioner who specialises in textiles." |
| **Context** | What's the situation and what do you know? | "We make performance fabrics. Our T-shirt is 100% polyester, knitted and dyed in China, sold in the EU." |
| **Task** | What exactly do you want? | "List every life cycle stage and the data we need for each." |
| **Format** | What should the answer look like? | "A table, then three sentences. Under 200 words." |
| **Checks** | How will we know it's right? | "List your assumptions first. Use code for any calculation." |

## Before and after

Asking for a number without context is the most common mistake in
sustainability work.

**Weak:**

```text
What is the carbon footprint of a polyester T-shirt?
```

You'll get one confident number, from nowhere, that could be off by a
factor of three.

**Strong:**

```text
You are an LCA practitioner who specialises in textiles. I'm a textile
technology manager, not an LCA expert.

Our product: a 140 g performance T-shirt, 100% polyester, filament yarn,
knitted, dyed and sewn in China, shipped by sea to a warehouse in Germany,
sold in the EU. (Made-up example.)

Map its life cycle from fibre to end of life. For each stage, list: the
activities, the data we'd need from suppliers, a typical unit (kWh per kg,
tonne-km...), and whether the stage is usually big or small for this kind
of product.

Format: one table, then the 3 stages to collect data for first.
Checks: don't give me any emission factor values yet; say where your
"usually big or small" comes from, and flag anything you're unsure of.
```

## Moves that separate good users from great ones

1. **Ask it to ask you questions first.** "Before you start, ask me up to 5
   questions that would improve your answer."
2. **Make it show its working.** "List your assumptions before the answer."
3. **Ask for options, not an answer.** "Give me three approaches with
   trade-offs" beats "what should I do?"
4. **Make it argue with itself.** "Now play devil's advocate against your own
   recommendation."
5. **Iterate like you would with a person.** "Shorter." "Less jargon." "Make
   the second option more aggressive." The first draft is never the last.
6. **Calculate with code.** "Write and run Python to calculate this" removes
   most arithmetic errors.
7. **Give it an example of what good looks like.** Paste a memo you liked and
   say "same structure and tone".
8. **Keep one chat per piece of work** so it remembers the context.

## Try it now (5 minutes)

Take a real (non-confidential) problem from your week, such as preparing for a
mill visit or a material review, and write a prompt using R-C-T-F-C. Then run it in two
different AI tools and compare. Log what you learned in your
[journal](../my-ai-journal.md).

**Next:** [3. You don't need to code](03-you-dont-need-to-code.md)
