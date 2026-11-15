# Exercise 2: Run an agent team by hand (no code)

**Goal:** understand how a team of AI agents works by **being the
orchestrator yourself**. You'll open three chats, give each one a role, and
pass work between them. This is exactly what the code in
[exercise 3](exercise-3-agent-team-in-colab.md) automates.

**Scenario:** the product team wants to cut the footprint of P01 Performance
T-shirt and P04 Sports leggings by at least 25% next season, and marketing
wants "25% lower carbon" on the hangtag.

## Set up three chats

Open three separate chats (they can be in different AI tools, which is even
better, because different models catch different mistakes). Paste one of
these at the start of each.

### Chat 1: Planner

```text
You lead a product sustainability review. I'll give you a brief. Turn it
into an analysis plan: 4 to 6 scenarios to test on our screening LCA model,
each with exact settings for: product, main fibre, mill country (where
yarn, fabric and dyeing happen), long-distance shipping (sea or air),
cutting waste %. Include single changes and combinations. Say what question
each scenario answers. Don't invent results. Later I'll bring you an
approved report and ask for the final memo.
```

### Chat 2: LCA Analyst

```text
You are an LCA analyst. I'll give you a plan with scenarios. I will run each
scenario in our screening model and paste the results to you. Your job is
to compare them: which scenarios reach -25% for each product, which levers
matter most, and the trade-offs (cost, supplier change, risk). Copy numbers
exactly and never estimate a number yourself. These are screening results,
not an ISO 14040/44 study.
```

### Chat 3: Critical Reviewer

```text
You are a sceptical critical reviewer of LCA work. I'll give you an
analyst's report plus the raw model results it is based on. Check: every
number in the report appears in the raw results; every planned scenario was
run; the conclusions follow from the numbers; and the report doesn't
over-claim (no public claims like "25% lower carbon" from a screening
model, no false certainty). Reply APPROVED, or REVISE with a numbered list
of specific fixes.
```

## Run the team

1. **Planner:** paste the brief:

   ```text
   Next season the product team wants to cut the screening footprint of P01
   Performance T-shirt and P04 Sports leggings by at least 25% each. Options:
   recycled polyester (P01 only), moving dyeing and finishing to Portugal or
   Turkey, shipping by sea instead of air, cutting waste down to 10%.
   Marketing would like to say "25% lower carbon" on the hangtag. Which
   combination reaches -25%, and what can we say publicly?
   ```

2. **You are the tool:** for each scenario in the plan, open the
   **LCA Explorer** (`dashboards/lca-explorer.html` on your GitHub Pages
   site), click the product, set the what-ifs, click **Copy summary for AI**,
   and paste the last paragraph ("Selected product with what-ifs") into a
   notes file. Label each one with its scenario. Click **Reset what-ifs**
   between scenarios.
3. **Analyst:** paste the plan and all the results.
4. **Reviewer:** paste the analyst's report *and* the raw results.
5. If the Reviewer says REVISE, paste its feedback to the Analyst, then send
   the new report back to the Reviewer. **Stop after one revision.**
6. **Planner:** paste the approved report and ask for a 300-word steering
   committee memo, including what we can and can't say publicly.

## Debrief questions (write the answers in your journal)

- Did the Reviewer catch anything? Would you have caught it?
- Which single lever got P04 past -25% on its own? Why can't recycled fibre
  alone do that for P01?
- Did anyone push back on the hangtag claim? What would you need before
  printing it?
- Where did you, as orchestrator, add judgement the agents couldn't (cost,
  supplier relationships, quality)?
- What would you **never** let an agent do without your approval at work?

## What you just learned

A team of agents is: **roles** (instructions), **tools** (the model),
**hand-offs** (you copying between chats), a **check** against evidence (the
Reviewer reading raw results), and a **stop rule** (one revision). In
exercise 3, Python does the copying.
