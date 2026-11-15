# Exercise 3: Build a real agent team in Google Colab

**Goal:** run the Planner → Analyst → Reviewer team from exercise 2 as real
agents. The Analyst calls the lifecycle model **by itself**, as a tool, and
the Reviewer checks its numbers against a log of every model run, and its
wording against the rule "no public claims from a screening".

**Cost:** free. It uses the Gemini API free tier from Google AI Studio (no
credit card), and runs in Google Colab (nothing to install).

**The code:** [agents/lca_agents.py](agents/lca_agents.py) ·
[open it in Google Colab](https://colab.research.google.com/github/jawdat-rana/learn-ai-for-textile/blob/main/part-2-advanced/agents/lca_agents.ipynb)

## Step 1: Try practice mode first (5 min)

Open the notebook in Colab and click **Runtime → Run all**. With no API key,
it runs in **practice mode**: the model results are real, but the agents'
words are canned. You'll see the hand-offs: plan → results → verdict →
memo. Read STEP 4 in the notebook: the agents are defined in plain English.

## Step 2: Get a free Gemini API key (10 min)

1. Go to **aistudio.google.com** and sign in with a Google account.
2. Click **Get API key → Create API key**. Copy it.
3. In Colab, click the **key icon** in the left sidebar (Secrets). Add a
   secret named `GEMINI_API_KEY`, paste the key as its value, and switch on
   **Notebook access**.
4. **Never** paste the key into the code or commit it to GitHub. Anyone with
   it can use your quota.

The free tier has daily limits and Google may use free-tier prompts to
improve its products, so only send made-up data like this course's. If you
get a "model not found" error, check the current free model names in AI
Studio and change `MODEL` in STEP 2.

## Step 3: Run the real team (10 min)

**Runtime → Run all** again. Now the Planner really decides which scenarios
to test, the Analyst really calls `run_lca_scenario`, and the Reviewer
really checks. STEP 6 shows how many times the Analyst called the model.
Compare the memo with the one you wrote by hand in exercise 2.

## Step 4: Change the team, in plain English (30 min)

Ask your AI chat to modify the notebook. Paste the code and one of these:

```text
Add a fourth agent, "Claims Reviewer", who reads the approved report and
drafts hangtag wording that is true and specific, or explains why we
shouldn't make a claim at all. Show me only the code to add.
```

```text
Give the Reviewer its own tool: a function that runs one scenario of the
model, so it can spot-check the Analyst independently.
```

```text
Add a "human approval" step: before the final memo, print the report and
ask me to type yes or no in Colab. If I type no, ask me what to change and
send it back to the Analyst.
```

```text
Add a "Data Collector" agent that reads the supplier answers in
prompt-kits/samples/supplier-responses.md and proposes which emission
factors to replace, with the converted values and its working. It must not
change the model itself; it only proposes.
```

## The prompt that produced the notebook

```text
Write a Google Colab notebook in Python that builds a team of three AI agents
using the google-genai library (Gemini API free tier), for a non-coder.

- Read the API key from Colab Secrets (GEMINI_API_KEY). If there's no key,
  run in "practice mode" with canned agent replies but real tool results,
  so I can see the flow.
- Tool: wrap the Module 1 lifecycle model (attached) as a Python function
  run_lca_scenario(product_id, fibre, mill_country, ship_by, cut_waste_pct)
  with a clear docstring, returning totals and stages before and after.
  Log every call.
- Agents: Planner (writes an analysis plan of 4-6 scenarios, later the final
  memo), Analyst (must call the tool for every scenario, never estimate),
  Reviewer (checks every number against the tool log and checks for
  over-claiming; replies APPROVED or REVISE with fixes).
- Flow: Planner → Analyst → Reviewer → at most one revision → Planner memo.
- Short numbered steps, plain-English comments, agent instructions easy to
  find and edit.
```

## Where AI is wrong

- **The Analyst may skip a scenario** or "estimate" instead of calling the
  tool. That's why the Reviewer gets the log, not just the report. Check
  STEP 6 yourself.
- **The Reviewer may approve too easily**, because it's the same model. Try
  making it stricter, or use a different model for it.
- **The memo may still sneak in a claim.** "Our tee is now 40% lower
  carbon" can reappear in the final memo even after the Reviewer objected.
  Read the memo yourself.
- **Free-tier limits.** If you see "quota exceeded" or a 429 error, wait a
  minute and run again. Don't build loops that retry forever.
- **The model changes.** Run the same notebook twice and the plan may
  differ. The tool results won't, which is exactly why numbers come from
  tools, not from the model.
