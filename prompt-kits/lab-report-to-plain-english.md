# Kit 4: Lab test report to plain English

**Use it when:** a test report lands (biodegradation, microfibre shedding,
restricted substances, colour fastness) and you need to explain what it
does and doesn't prove to product, marketing or management.

**Try it with:** [samples/test-report.md](samples/test-report.md), a made-up
marine biodegradation report with several limits hidden in the detail.

> Real test reports can be confidential. Remove the client and lab names
> before pasting, and use only AI tools your company allows.

## The prompt

```text
You are a textile testing specialist explaining a lab report to a product
director who isn't a chemist. From the report below:

1. Summarise in 3 sentences what was tested, how, and the result.
2. Make a table: what the report PROVES | what it does NOT prove | why.
   Consider: the material tested vs the finished product (dyes, finishes,
   blends), test conditions vs real environments, duration, pass criteria,
   sample size, and whether a reference material behaved as expected.
3. List the claims we could and could not make based on this report alone.
4. List follow-up tests or questions for the lab.

Quote the report for every point. Don't add facts that aren't in the
report; if you think a standard requires something, say "check the
standard" rather than stating it as fact.

[paste report]
```

## What good looks like (for the sample)

It should notice that the test used **un-dyed, un-finished fibre**, not the
finished fabric; that it ran at **30 °C in a lab**, warmer than most real
seawater; that **62% biodegradation after 180 days** is not "fully
biodegradable"; that **only 3 replicates** were used and one is noticeably
lower; that **no ecotoxicity test** of the residue was done; and that the
report itself says results "may not be extrapolated to other environments".
It should say a claim like "ocean safe" isn't supported by this report alone.

## Where AI is wrong

- **It upgrades results.** "Showed significant biodegradation" turns into
  "biodegradable" in the summary. Compare the summary with the numbers.
- **It invents standard requirements.** Pass thresholds and durations are
  specific to each standard and version. Check the standard.
- **It misses footnotes.** Limits are often in small print at the end.
  Ask: "What do the notes and limitations section say?"

## Make it yours

Keep a list of the standards your company uses, with the pass criteria from
the official documents, and paste it into the prompt.
