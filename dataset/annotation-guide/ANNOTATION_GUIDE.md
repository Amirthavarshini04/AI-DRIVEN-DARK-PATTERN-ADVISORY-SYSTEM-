# Dataset Annotation Guide: Indian E-Commerce Dark Patterns (CCPA 2023 Guidelines)

## 1. Overview
This annotation protocol defines labeling guidelines for identifying manipulative user-interface patterns (Dark Patterns) on Indian e-commerce and quick-commerce websites in English, Hindi (हिंदी), and Tamil (தமிழ்).

## 2. Guideline Categories (CCPA Guidelines 2023)
Annotate snippets under the following 13 official CCPA categories:
1. **False Urgency**: Artificial countdown timers, fake stock numbers ("Only 2 left").
2. **Basket Sneaking**: Auto-prechecked insurance, donation, or service fees added to cart.
3. **Confirm Shaming**: Emotional guilt text in opt-out choices ("No, I prefer paying full price").
4. **Forced Action**: Gating basic features behind unrelated newsletter/app downloads.
5. **Subscription Trap**: Hard-to-cancel auto-renewal memberships.
6. **Interface Interference**: Low contrast decline buttons, visual hierarchy manipulation.
7. **Bait and Switch**: Changing advertised price at checkout.
8. **Drip Pricing**: Concealed convenience/handling fees revealed at payment stage.
9. **Disguised Ads**: Ads formatted like organic product recommendations or system alerts.
10. **Nagging**: Intrusive repetitive popups after user refusal.
11. **Trick Wording**: Double negatives, confusing inverted opt-out checkboxes.
12. **SaaS Billing**: Auto-converting free trial to paid card charge without notice.
13. **Deceptive Counting**: Fake live viewer/purchase counts ("5,000 bought in last 1 hr").

## 3. Annotation Protocol
- **Text Snippet**: Exact visible text string extracted from DOM.
- **Severity**:
  - `Critical`: Direct financial loss (Drip Pricing, Bait & Switch).
  - `High`: Immediate decision pressure (False Urgency, Basket Sneaking, Forced Action).
  - `Medium`: Emotional manipulation (Confirm Shaming, Trick Wording).
  - `Low`: Minor interface interference.
- **Language**: `en`, `hi`, `ta`.
