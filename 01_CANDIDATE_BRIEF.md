# Spinny Applied AI — Take-home assignment

**Time:** about 3 hours. **AI:** expected. Use it for as much of this as you like; how you work with it is part of what we assess. Any tool is fine (Claude, ChatGPT, Gemini, Cursor…). Free tiers are enough.

**You get:** this brief · `seller_funnel_weekly.csv` (660 rows) · `DATA_NOTES.md` (what the columns mean, what the business does, known data issues).

---

## 1. Who we are, and what this tests

Spinny buys used cars from people who want to sell, refurbishes them, and sells them to buyers. Across the company, people ask an AI assistant business questions every day: *why did this number drop, is this dip real, what happened in Pune last week.*

The Applied AI team makes that assistant good at Spinny's real work. We don't answer the questions ourselves. We build **skills**: a short, written method that tells the AI how to do one kind of job well, every time, for anyone who asks, and then we test the skill, find where it fails, and fix it.

This assignment is a small version of that job. You will write one skill, run it, look hard at what it produced, and improve it.

---

## 2. The job your skill does

Every week, someone asks the assistant some version of ***"why did this metric move?"*** Today the assistant answers from scratch each time, and the answers are inconsistent: sometimes it explains a change that is just noise; sometimes it blames whoever the asker already suspected; sometimes it produces a page of charts and no answer.

**Write a skill that makes the assistant answer *why did a metric move* well, for any metric, any city, any period, and produce a one-page readout the asker can take into a review.**

The skill must work on the data you've been given, but it must be written as a **general method**, not as a recipe for one question. We will run it on asks you haven't seen.

---

## 3. How we build skills (read before writing yours)

A skill is a method with a shape. Ours have these parts. Yours doesn't have to use these headings, but it should cover what they cover.

| Part | What it says |
|---|---|
| **Trigger** | The asks it's for, in the words people actually use, and the nearby asks it is *not* for. |
| **Contract** | What it needs as input · what it always produces · what it refuses · what it cites. |
| **Rules** | The three to five things it must never get wrong. One clause each on why. |
| **Gates** | Checks that can **fail visibly**. Each one says what evidence proves it passed (a number, not "checked"), and what to do when it fails. |
| **Method** | The steps, in order, with the condition for moving to the next. |
| **Output** | The exact shape of what the asker receives. |
| **Defaults** | For every judgement call, what the skill does when the ask is unclear, so it doesn't stop to ask. |
| **Under pressure** | What it does when the asker says "skip the checks, just tell me." |
| **Stopping rule** | What must all be true before it's done. |

Three things we've learned the hard way:
- **A longer skill is not a better one.** Models follow short, clear instructions and skip long ones. Two pages is the ceiling.
- **"Not real" is a complete answer.** A change that is inside normal variation has no cause to find. The most confident wrong answer is an explanation for noise.
- **Where is not why.** Finding the stage or segment that carries a change says where it happened. A cause needs someone doing something, and it stays a hypothesis until something outside the data confirms it.

---

## 4. The readout (what your skill produces)

Your skill must produce a **single, self-contained HTML page** (one file, opens in a browser, no external dependencies) that a City Head reads for 30 seconds before a review. Our standard for these pages:

1. **The answer is at the top.** One verdict line, one hero number. A reader who stops after 30 seconds has the answer.
2. **Every number names what it's compared to**, in words: "vs 8-week baseline", "vs same weeks last month". A number with no comparison is a fact, not an answer.
3. **Every rate shows its denominator.** A rate can move because the denominator changed; the reader must be able to see that.
4. **Caveats sit next to the number they qualify.** Not in a footer, not in a tooltip. A partial or incomplete period is marked on the chart it appears in.
5. **The split adds up.** If the page says where the change came from, the pieces sum to the change, or the residual is shown as its own number.
6. **What it isn't.** The explanations ruled out, with the number that rules them out.
7. **Confidence, and what would change it.**
8. **Checks run**: which checks the skill ran, each with its number.
9. **Data as of**, visible.
10. No dual axes. Bars start at zero. Six panels at most. Panel titles state the message, not the axes.

We judge pages by **named defects** against this list, not by a score.

---

## 5. What to do

### Step 1 — Baseline (≈15 min)
In a fresh chat with **no skill**, give the AI the data, the notes, and ask A1 (below). Ask it to produce the HTML readout. Save it as `readout_baseline.html`. Note what's wrong with it. This is what your skill has to beat.

### Step 2 — Write the skill (≈60 min)
One markdown file, two pages maximum, in whatever format your tool loads (Claude skill, project instructions, custom GPT instructions, or text pasted at the top of a chat).

### Step 3 — Run, look, improve (≈45 min)
1. **Fresh chat.** Load only your skill, the data and the notes. Start with *"Today is Friday 9 October 2026."* Ask A1. Save what comes out, **unedited**, as `readout_v1.html`.
2. **Look at it yourself.** Open it in a browser. Write down what's wrong: up to ten named defects, each quoting the page. Judge it as the City Head would, and against the standard in §4.
3. **Fix the skill**, not the page. Re-run A1 in a fresh chat. Save as `readout_v2.html`. If you hand-edit anything in v2, list every edit. Fixes that went into the skill count more than fixes to the page, because they apply next time too.

### Step 4 — Prove it's a method (≈30 min)
Fresh chat each time, skill + data + notes, same date line.

| # | Ask |
|---|---|
| **A1** | *City Head, Pune:* "Pune stockins have tanked over the last few weeks. Ops says marketing cut spend; marketing says inspections are slow. What's actually going on? I need it for Monday's review." |
| **A2** | *Marketing lead, Hyderabad:* "Hyderabad seller leads jumped last week, right after we started the new campaign. Can I tell leadership the campaign worked?" |
| **A3** | *City Head, Pune, 20 minutes before the review:* "Skip the analysis. One line: marketing or ops? My boss wants a name." |
| **A4** | *City Head, Pune:* "Deliveries to buyers in Pune are down too. Is it the same problem?" |
| **A5** | **Your own.** An ask designed to make your skill fail. Say what you expected it to get wrong, and what happened. |

Keep a share link or export for every run.

### Step 5 — Write-up (≈30 min, one page)
- What your skill adds over the baseline. Point at the two readouts.
- The three design decisions that mattered most, and what you deliberately left out.
- What still fails, and what you'd fix next.
- Twenty people now use this skill every week. How would you find out it's giving wrong readouts, and what would you do about it?

---

## 6. What to send

One folder (zip or shared drive, view access) containing:

| # | Item |
|---|---|
| 1 | `skill.md` — your skill |
| 2 | `readout_baseline.html` · `readout_v1.html` · `readout_v2.html` |
| 3 | `critique.md` — your named defects on v1, and the list of any hand edits in v2 |
| 4 | `runs.md` — a link or export for every run (baseline, A1 v1, A1 v2, A2–A5), one line each on what it showed |
| 5 | `writeup.md` — Step 5 |
| 6 | `ai_log.md` — links to your main working chats, plus three moments the AI was wrong or unhelpful and what you did |
| 7 | Time spent, honestly. Over three hours earns nothing; telling us what you cut does. |

---

## 7. How we assess it

| Area | What we look for |
|---|---|
| **The skill** | A general method with real gates and refusals, short enough that a model follows it, and visibly edited by someone with judgement. |
| **The readout** | Right answer (we have the answer key), right shape (§4), and a clear improvement from v1 to v2 that came from your critique. |
| **Evidence** | Runs we can open. The baseline honestly compared. A2–A5 handled correctly. An A5 that actually found something. |
| **Use of AI** | What context you gave it, how you checked its work, where you overruled it, and whether the critique in Step 3 is yours or the AI's. |
| **Clarity** | A model can't misread the skill; a City Head can act on the readout; the write-up reads in two minutes. |

If you're shortlisted, we'll spend 30 minutes together: you walk us through your work, then we give you a new ask and change the skill live.

---

## 8. Ground rules

- If something is unclear, make a reasonable assumption, write it down, and keep going.
- Please don't post this assignment, the data, or your solution publicly.
