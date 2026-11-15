# Kit 2: Green claims check

**Use it when:** marketing copy, a hangtag, a product page or a sales deck
mentions the environment, and you want a first check before it goes to
legal or compliance.

**Try it with:** [samples/marketing-claims.md](samples/marketing-claims.md),
ten made-up claims, from fine to clearly risky.

> This is a first pass to help you ask better questions, not legal advice.
> Rules differ by market and change often. In the EU, Directive (EU)
> 2024/825 restricts generic environmental claims from 27 September 2026.
> Always check with your legal team.

## The prompt

```text
You are a sustainability communications reviewer for a textile brand that
sells in [the EU]. For each claim below:

1. Classify it: generic (e.g. "eco-friendly"), specific and measurable,
   comparative, about the future, or based on offsetting.
2. Say what evidence would be needed to support it, and from whom.
3. Rate the risk: High / Medium / Low, with one line of why.
4. Suggest a safer rewrite that says something true, specific and
   checkable, or recommend deleting it.

Rules: don't assume we have evidence we haven't mentioned. Quote the exact
claim each time. If a claim depends on a specific law, name the law and tell
me to check its current text rather than quoting it from memory.

Evidence we actually have: [e.g. a screening LCA, not ISO-reviewed;
GRS certificate for recycled polyester in style P06; no biodegradation tests]

[paste the claims]
```

## What good looks like (for the sample)

It flags **"eco-friendly"** and **"kind to the planet"** as generic claims;
**"carbon neutral thanks to our offset partner"** as an offset-based product
claim; **"30% lower carbon footprint"** as a comparative claim needing a
verified study (a screening LCA isn't enough); **"biodegradable"** and
**"ocean safe"** as needing environment-specific test evidence; and
**"we will be net zero by 2035"** as a future claim needing a plan with
targets. It should be comfortable with **"Made with 85% recycled polyester
(GRS certified)"** if the certificate exists, and suggest stating what the
other 15% is.

## Where AI is wrong

- **It quotes laws from memory.** Article numbers and dates can be wrong or
  out of date. Paste the official text or check it.
- **It's either too strict or too relaxed.** Some AIs flag everything; some
  rewrite a risky claim into a slightly less risky one. Ask: "Would this
  rewrite still be a problem without evidence?"
- **It forgets the evidence you don't have.** It may write "backed by our
  LCA" when your LCA is a screening. Tell it what you actually have.
- **Pictures and names count.** Leaves, green colours and product names like
  "EcoTee" can be claims too. The AI only sees the text you paste.

## Make it yours

Add your company's claims policy and your list of certificates to the prompt.
