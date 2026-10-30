# Data notes — `seller_funnel_weekly.csv`
*Everything here is invented for this exercise: the numbers, the cities, the data issues, the people.*

## What the business does
Spinny buys used cars from people who want to sell, refurbishes them, and sells them to buyers. This file covers the **seller side** only. Buyer-side activity (test drives, bookings, deliveries) is a different funnel and is not in this data.

## The seller funnel
A **seller lead** comes in → an inspector **inspects** the car → Spinny **makes an offer** → if the seller accepts, the car is **stocked in**. A stockin is the main supply number each city is measured on.

What moves stockins, and who owns each lever:

| Lever | Metric | Owner |
|---|---|---|
| Lead volume, by channel | `leads` | Marketing (also owns spend, which is **not in this file**) |
| Inspection rate | `inspections_done ÷ leads` | City ops |
| Offer rate | `offers_made ÷ inspections_done` | Inspection quality / policy |
| Stockin rate | `stockins ÷ offers_made` | Mostly the gap between Spinny's offer and the seller's expected price → Pricing team |

## The file
One row per **week × city × channel × car age band**. Weeks start Monday. **Data as of Thu 8 Oct 2026** (last complete day): the week of 5 Oct has **4 of 7 days**.

| Column | Meaning |
|---|---|
| `week_start` | Monday of the week the lead was **created** |
| `city` | Pune · Hyderabad · Bengaluru · Delhi NCR |
| `channel` | paid_digital · organic · referral · partner (· unknown, see notes) |
| `car_age_band` | 0-3y · 4-6y · 7y+ |
| `leads` | seller leads created that week |
| `inspections_done` | of those leads, how many were inspected (so far) |
| `offers_made` | of those, how many received an offer (so far) |
| `stockins` | of those, how many Spinny has bought (so far) |
| `avg_offer_price` | average offer Spinny made, ₹ |
| `avg_expected_price` | average price the seller said they expected, ₹ |

**Everything is attributed to the lead's creation week.** A lead can be inspected, offered and stocked in up to **14 days** after it is created; about 70% of eventual stockins happen within the first 7 days. So the most recent weeks have not finished converting.

## Known data issues
- **Pune, 7–13 Sep:** an app release stopped inspection completions being logged for most of the week. Inspections happened as normal; offers and stockins were recorded correctly. Fixed 14 Sep. Not backfilled.
- **Bengaluru, before 3 Aug:** a tracking change means ~15% of leads carry `channel = unknown`. Volume is correct; channel split is not.
- **Marketing spend, campaign dates, pricing-policy changes, inspector headcount:** not in this file. The teams that own them have them.

