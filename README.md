# Learn AI with use cases: AI for textile professionals

A free, hands-on course for **textile technology, product and sustainability
managers who don't code**. You'll use free AI tools to run a screening-level
**product lifecycle analysis (LCA)** in-house, compare material substitutions,
and leave with work you could show your leadership team.

> **The big idea:** you don't need to know how to program. You think of the
> use case and describe it well. The AI writes the code, explains it and fixes
> it. Your job is the part AI can't do: knowing the textile process and judging
> whether the answer is right.

**Website:** [jawdat-rana.github.io/learn-ai-for-textile](https://jawdat-rana.github.io/learn-ai-for-textile/)
(your own copy gets its own address)

---

## Why this course

A full LCA from an external consultancy costs a lot and takes months. Much of
the early work is something you can do yourself with AI: map the life cycle,
collect the data, find the hotspots, test what-ifs and decide **where a
consultant's time is really worth paying for**. This course shows you how,
and is honest about where in-house screening stops and a certified study
has to start.

| You can do in-house with this course | You still need an expert or certified study for |
|---|---|
| A screening carbon footprint for each product, by life cycle stage | Claims on labels, websites or in tenders |
| Finding the hotspots and the data that matters most | Comparing your product with a competitor's in public |
| What-ifs: new fibre, new dye house, sea instead of air | ISO 14040/44 critical review, EU PEF studies |
| A sharp brief that makes a consultant's quote cheaper and faster | Water, toxicity and land-use impacts done properly |

## How it works

1. **Copy the course** into your own free GitHub account and switch on your
   own website. → [START-HERE.md](START-HERE.md) (15 minutes, no installing)
2. **Learn the foundations** in four short lessons, including LCA in 15 minutes.
3. **Do the two flagship projects** with a free AI tool (Claude, ChatGPT or
   Gemini). Every step has a copy-paste prompt.
4. **Run the code without coding:** in the AI chat, or in Google Colab with
   one click.
5. **Publish** interactive dashboards on your own GitHub Pages site.
6. **Keep a journal** of what worked and where the AI was wrong.

No paid subscriptions needed. All products, companies and suppliers are made
up, so the data is safe to upload anywhere. Emission factors are public values
with [sources](SOURCES.md).

## The course

### Foundations (45 minutes)

1. [How AI chat tools work, in 10 minutes](00-foundations/01-how-ai-works.md):
   what they're good and bad at, and what never to paste in
2. [Prompting for technical leaders](00-foundations/02-prompting-for-technical-leaders.md):
   the Role, Context, Task, Format, Checks pattern
3. [You don't need to code (but you'll use code)](00-foundations/03-you-dont-need-to-code.md):
   how to get AI to write, run, explain and fix code for you
4. [LCA in 15 minutes](00-foundations/04-lca-in-15-minutes.md): functional
   unit, system boundary, emission factors, and screening vs ISO studies

### Flagship projects

| | Project | You'll produce | AI skills you'll learn |
|---|---|---|---|
| 1 | [**Product Lifecycle Screening**](module-1-product-lca/README.md) | A cradle-to-grave carbon footprint for six products, a hotspot chart, a sensitivity check, what-ifs, an internal summary and a consultant brief | Turning a process into a model, checking data before maths, sourcing factors honestly, testing what moves the answer |
| 2 | [**Material Substitution Explorer**](module-2-material-substitution/README.md) | A comparison of six fibre options for one T-shirt, per garment and per wear, with ranges and a beyond-carbon scorecard | Choosing the right unit of comparison, uncertainty ranges, weighing trade-offs, spotting unsupported claims |

Each project has:

- `prompts.md`: every prompt, including **the prompts that generated the code**
- `analysis/*.py` and `*.ipynb`: the Python the AI wrote, runnable in Google Colab
- an interactive dashboard (HTML and JavaScript) on your GitHub Pages site
- a **"Where AI is wrong"** section, because sustainability numbers need to be
  trusted carefully, not blindly

### Prompt kits (reuse every week)

| Kit | For |
|---|---|
| [Supplier sustainability data check](prompt-kits/supplier-sustainability-data-check.md) | Turning supplier questionnaire answers into a data-gap list and follow-up emails |
| [Green claims check](prompt-kits/green-claims-check.md) | Testing marketing copy before it goes out |
| [LCA scope and consultant brief](prompt-kits/lca-scope-and-consultant-brief.md) | Writing a goal-and-scope brief so external quotes are comparable and cheaper |
| [Lab test report to plain English](prompt-kits/lab-report-to-plain-english.md) | Biodegradation, shedding or chemical test reports, for non-specialists |

### Part 2 (advanced): skills, agents and AI teams

[Part 2](part-2-advanced/README.md) is a bonus for when you've finished the
above: package your LCA method as a reusable **skill**, run an **agent team**
by hand (Data Collector → LCA Analyst → Critical Reviewer), then build a real
team of agents in Google Colab with a free API key.

### Keep going

- [The 10 challenges](challenges.md): tick them off as you go
- [My AI journal](my-ai-journal.md): edit it in your browser after each session

---

## What's in the repository

```text
START-HERE.md                    Set up GitHub, your copy and your website
00-foundations/                  Four short lessons
module-1-product-lca/            Flagship 1: data, factors, prompts, Python, example outputs
module-2-material-substitution/  Flagship 2: options, prompts, Python, example outputs
prompt-kits/                     Four reusable prompts with made-up samples
part-2-advanced/                 Skills, agents and AI teams (bonus)
dashboards/                      Interactive HTML/JavaScript dashboards for GitHub Pages
SOURCES.md                       Every emission factor source, and how far to trust it
index.html, assets/              The course website
challenges.md, my-ai-journal.md
tools/                           For the course owner: checks JavaScript and Python agree
```

## A word on data, claims and safety

- Products, companies and suppliers here are **made up**. Emission factors
  are public, rounded and sourced in [SOURCES.md](SOURCES.md).
- Your copy of the course is **public**. Never commit company data to it:
  bills of materials, supplier names, energy bills and costs are confidential.
- At work, use only AI tools your company has approved, and follow its data
  policy. Free consumer AI tools may keep what you paste.
- Screening results are for internal decisions. **Don't put them on a label,
  website or sales deck.** In the EU, generic environmental claims are
  restricted (see [SOURCES.md](SOURCES.md)).
- AI output is a draft. You're accountable for what you send.

---

## For the course owner

To let friends copy the course with **Use this template**, open this
repository's **Settings → General** and tick **Template repository**. To
publish the course website, go to **Settings → Pages** and deploy from the
`main` branch, `/ (root)` folder.

If you change the model or the data, run both Python scripts and then
`node tools/check_numbers.js` to confirm the dashboards and notebooks still
agree.
